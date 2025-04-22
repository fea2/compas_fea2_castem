from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_fea2
from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ModalAnalysis


class CastemModalAnalysis(ModalAnalysis):
    """Castem implementation of Modal Analysis step.

    The VIBR method is used for the resolution of (K-(2*PI*f)^2M).u = 0.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=VIBR

    The rigidity and mass matrix are generated with the RIGI et MASS operators.

    The 'INTERVALLE' method of resolution of the VIBR operator is implemented.
    The other methods are not implemented yet.

    """

    __doc__ += ModalAnalysis.__doc__

    def __init__(
        self,
        *,
        modes=1,
        **kwargs,
    ):
        super(CastemModalAnalysis, self).__init__(modes, **kwargs)

    def jobdata(self):
        return f"""*
{self._generate_header_section()}
* - Analysis Parameters
*   -------------------
{self._generate_analysis_section()}
*
* - Output Results
*   --------------
{self._generate_output_section()}
*
"""

    def _generate_header_section(self):
        return f"""*
* STEP {self.name}
*"""

    def _generate_analysis_section(self):
        return f"""
RIG1 = RIGI MODTOT MATTOT;
RIGTOT = RIG1 ET CLTOT;
MASTOT = MASS MODTOT MATTOT;

TABRES = VIBR INTER 0. 1000. BASSE {self.modes} RIGTOT MASTOT;
"""

    def _generate_output_section(self):
        return f"""
****************** EIGENVALUES ******************
TABEIGVAL = VIDE 'TABU' (MOTS 'MODE' 'LAMB' 'OMEG' 'FREQ' 'PERI') 'LISTENTI'*1 'LISTREEL'*4;
PI = 3.14159265359;

REPE BOUC1 {self.modes};
    TABEIGVAL.MODE = TABEIGVAL.MODE ET &BOUC1;
    FREQI = TABRES.MODES.(&BOUC1).FREQUENCE;
    OMEI = FREQI*2*PI;
    LAMBI = OMEI**2;
    PERII = 1 / FREQI;
    
    TABEIGVAL.LAMB = TABEIGVAL.LAMB ET LAMBI;
    TABEIGVAL.OMEG = TABEIGVAL.OMEG ET (FREQI*2*PI);
    TABEIGVAL.FREQ = TABEIGVAL.FREQ ET FREQI;
    TABEIGVAL.PERI = TABEIGVAL.PERI ET (1/FREQI);
FIN BOUC1;

OPTI SORT '{self.problem.path}\\eigenvalues';
SORT  'EXCE' TABEIGVAL 'SEPA' 'ESPA';

****************** EIGENVECTORS ******************
*Extraction of the name and nb of dofs per point
RESEIG = REDU TABRES.MODES.(1).DEFORMEE_MODALE MAILTOT;
LCOMP = EXTR RESEIG 'COMP';
NCOMP = DIME LCOMP;

TABM = TABLE;
REPETER BOUCM NCOMP;
    TABM.(&BOUCM) = EXTR LCOMP &BOUCM;
FIN BOUCM;

TABEIGVEC = VIDE 'TABU' ((MOTS 'KEY' 'MODE') ET LCOMP) 'LISTENTI'*2 'LISTREEL'*NCOMP;

REPE BOUC1 {self.modes};
    NPOINT = DIME TABPOINTS.POINT;

    REPETER BOUC2 (NPOINT);
        POINTi = TABPOINTS.POINT.(&BOUC2-1);
        KEYi = TABPOINTS.KEY.(&BOUC2-1);
        TABEIGVEC.KEY = TABEIGVEC.KEY ET (LECT KEYi);
        TABEIGVEC.MODE = TABEIGVEC.MODE ET (LECT &BOUC1);

        REPETER BOUC3 NCOMP;
            MOTi = TABM.&BOUC3;
            VALi = EXTR TABRES.MODES.(&BOUC1).DEFORMEE_MODALE MOTi POINTi;
            TABEIGVEC.MOTi = TABEIGVEC.MOTi ET (PROG VALi);
        FIN BOUC3;

    FIN BOUC2;

FIN BOUC1;

OPTI SORT '{self.problem.path}\\eigenvectors';
SORT  'EXCE' TABEIGVEC 'SEPA' 'ESPA';

"""


class CastemBucklingAnalysis(BucklingAnalysis):
    """Castem implementation of Modal Analysis step.

    Castem can only do buckling analysis with a preloaded step.



    """

    __doc__ += BucklingAnalysis.__doc__

    def __init__(
        self,
        modes=1,
        max_increments=1,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=False,
        t_under_inc=0.1,
        max_under_increments=10,
        load_step=1,
        **kwargs,
    ):
        super(CastemBucklingAnalysis, self).__init__(**kwargs)

        self.modes = modes
        self.max_increments = max_increments
        self.initial_inc_size = initial_inc_size
        self.min_inc_size = min_inc_size
        self.time = time
        self.nlgeom = nlgeom
        self.modify = modify
        self.t_under_inc = t_under_inc
        self.max_under_increments = max_under_increments
        self.load_step = load_step

    def jobdata(self):
        return f""" 

{self._generate_header_section()}
* buckling

***************STATIC ANALYSIS***************
***
*** - LOADS
***   -------------------
*** Evolution of loading
TCAL = PROG 0. 'PAS' {self.t_under_inc} 1.;
TSAUV = PROG 0. 'PAS' {self.t_under_inc} 1.;

LISTEMP = PROG 0. 'PAS' 1. {int(1 / self.load_step)};
LISC = PROG 0. 'PAS' {self.load_step} 1.;
EVOLC = EVOL MANU 'TIME' LISTEMP 'CHARGE' LISC;

CHARTOT = VIDE 'CHARGEME';
***
*** - Loads & Displacements
***   -------------

{self._generate_loads_displacement_section()}

*** - ANALYSIS
***   -------------------
***
TAB3 = TABLE ;
TAB3.MODELE = MODTOT ET MODJTOT;
TAB3.CARACTERISTIQUES = MATTOT ET MATJTOT;
TAB3.BLOCAGES_MECANIQUES = CLTOT ET CONTOT ET CRIGTOT;
TAB3.CHARGEMENT = CHARTOT;
TAB3.TEMPS_SAUVES = TSAUV;
TAB3.TEMPS_CALCULES = TCAL;
TAB3.MAXSOUSPAS = {self.max_under_increments};
TAB3.MAXITERATION = {self.max_increments};
TAB3.PRECISION = {self.min_inc_size};
TAB3.GRANDS_DEPLACEMENTS = {"VRAI" if self.nlgeom else "FAUX"};
TAB3.CONVERGENCE_FORCEE= FAUX;


PASAPAS TAB3;

NCONTRAINTES = DIME TAB3.CONTRAINTES;

***************BUCKLING ANALYSIS*************

TAB2 = TABLE;
TAB2.'OBJM' = MODTOT ET MODJTOT ;
TAB2.'LAM1' = 0.01;
TAB2.'LAM2' = 100.;
TAB2.'NMOD' = {self.modes};
TAB2.'CLIM' = CLTOT ET CONTOT ET CRIGTOT;
TAB2.'SIG1' = TAB3.CONTRAINTES.(NCONTRAINTES-1); 
TAB2.'MATE' = MATTOT;

TABBUCK = FLAMBAGE TAB2:;
*
* - Output Results
*   --------------
{self._generate_output_section()}
*
"""

    def _generate_header_section(self):
        return f"""*
* STEP {self.name}
*"""

    def _generate_output_section(self):
        return """*
"""

    def _generate_loads_displacement_section(self):
        field_data = []
        for field in self.load_fields:
            if isinstance(field, compas_fea2.problem.DisplacementField):
                field_data.append(field.jobdata())
            else:
                field_data.append(self.combination.jobdata())

        return "\n".join(field_data)

    def _generate_loads_section(self):
        return self.combination.jobdata()
