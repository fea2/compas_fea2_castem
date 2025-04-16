from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ModalAnalysis


class CastemModalAnalysis(ModalAnalysis):
    #  __doc__ += ModalAnalysis.__doc__

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
    # buckling can't be done without doing a static analysis before ??
    """"""

    def __init__(self, **kwargs):
        super(CastemBucklingAnalysis, self).__init__(**kwargs)

    def jobdata(self):
        return f"""
{self._generate_header_section()}
* buckling
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
        return f"""*
TAB2 = TABLE;
TAB2.'OBJM' = MODTOT;
TAB2.'LAM1' = 0.01;
TAB2.'LAM2' = 100.;
TAB2.'NMOD' = {self.modes};
TAB2.'CLIM' = CLTOT;
TAB2.'SIG1' = TAB3.CONTRAINTES.(NCONTRAINTES-1); 
TAB2.'MATE' = MATTOT;

"""

    def _generate_output_section(self):
        return """*
"""
