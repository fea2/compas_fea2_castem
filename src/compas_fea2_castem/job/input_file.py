from datetime import datetime

import compas_fea2
from compas_fea2.job import InputFile

import compas_fea2_castem


class CastemInputFile(InputFile):
    """Input file object for standard analysis.

    Parameters
    ----------
    problem : obj
        Problem object.

    Attributes
    ----------
    name : str
        Input file name.
    job_name : str
        Name of the Castem job. This is the same as the input file name.
    data : str
        Final input file text data that will be written in the .dgibi file.
    """

    def __init__(self, problem, **kwargs):
        super().__init__(problem, **kwargs)
        self._extension = "dgibi"
        self.procedures = f"""
*post-treatment procedure creating a table contening the key and corresponding results of a node
*entry : champs par point des résultats
DEBP CHPOTAB CHOUT*'CHPOINT' LCOMP*'LISTMOTS' TABPO*'TABLE';
    NMOT = DIME LCOMP;
    TABO =  VIDE 'TABU' ((MOTS 'KEY') ET LCOMP) 'LISTENTI'*1 'LISTREEL'*NMOT;

    TABM = TABLE;
    REPETER BOUCM NMOT;
        TABM.(&BOUCM) = EXTR LCOMP &BOUCM;
    FIN BOUCM;

    NPOINT = DIME TABPO.POINT;
    REPETER BOUC1 (NPOINT);
        POINTi = TABPO.POINT.(&BOUC1-1);
        KEYi = TABPO.KEY.(&BOUC1-1);
        TABO.KEY = TABO.KEY ET (LECT KEYi);
        REPETER BOUC2 NMOT;
            MOTi = TABM.&BOUC2;
            VALi = EXTR CHOUT MOTi POINTi;
            TABO.MOTi = TABO.MOTi ET (PROG VALi);
        FIN BOUC2;
    FIN BOUC1;
FINP TABO;

DEBP SFTAB CHCONT*'MCHAML' TABEL*'TABLE';
*initialization of the output table
    TABO =  VIDE 'TABU' (MOTS 'KEY' 'FX1' 'FY1' 'FZ1' 'MX1' 'MY1' 'MZ1'
    'FX2' 'FY2' 'FZ2' 'MX2' 'MY2' 'MZ2') 'LISTENTI'*1 'LISTREEL'*12;

*the values are extracted element by element
    NELE = DIME TABELE.(0).ELE;
    REPETER BOUC1 (NELE);
        ELEi = TABELE.(0).ELE.(&BOUC1-1);
        KEYi = TABELE.(0).KEY.(&BOUC1-1);
        TABO.KEY = TABO.KEY ET (LECT KEYi);

* extraction of the values in the CHAM
        VALi1FX = EXTR CHCONT 'EFFX' 1 &BOUC1 1;
        VALi2FX = EXTR CHCONT 'EFFX' 1 &BOUC1 2;
        TABO.FX1 = TABO.FX1 ET (PROG VALi1FX);
        TABO.FX2 = TABO.FX2 ET (PROG VALi2FX);

        VALi1FY = EXTR CHCONT 'EFFY' 1 &BOUC1 1;
        VALi2FY = EXTR CHCONT 'EFFY' 1 &BOUC1 2;
        TABO.FY1 = TABO.FY1 ET (PROG VALi1FY);
        TABO.FY2 = TABO.FY2 ET (PROG VALi2FY);

        VALi1FZ = EXTR CHCONT 'EFFZ' 1 &BOUC1 1;
        VALi2FZ = EXTR CHCONT 'EFFZ' 1 &BOUC1 2;
        TABO.FZ1 = TABO.FZ1 ET (PROG VALi1FZ);
        TABO.FZ2 = TABO.FZ2 ET (PROG VALi2FZ);

        VALi1MX = EXTR CHCONT 'MOMX' 1 &BOUC1 1;
        VALi2MX = EXTR CHCONT 'MOMX' 1 &BOUC1 2;
        TABO.MX1 = TABO.MX1 ET (PROG VALi1MX);
        TABO.MX2 = TABO.MX2 ET (PROG VALi2MX);

        VALi1MY = EXTR CHCONT 'MOMY' 1 &BOUC1 1;
        VALi2MY = EXTR CHCONT 'MOMY' 1 &BOUC1 2;
        TABO.MY1 = TABO.MY1 ET (PROG VALi1MY);
        TABO.MY2 = TABO.MY2 ET (PROG VALi2MY);

        VALi1MZ = EXTR CHCONT 'MOMX' 1 &BOUC1 1;
        VALi2MZ = EXTR CHCONT 'MOMX' 1 &BOUC1 2;
        TABO.MZ1 = TABO.MZ1 ET (PROG VALi1MZ);
        TABO.MZ2 = TABO.MZ2 ET (PROG VALi2MZ);
    FIN BOUC1;
FINP TABO;


DEBP STRESSTAB CHCONT*'MCHAML';

    LCOMP = EXTR CHCONT COMP;
    NBPART = {len(self.model.parts)};
    NMOT = DIME LCOMP;

    TABO =  VIDE 'TABU' ((MOTS 'KEY') ET LCOMP) 'LISTENTI'*1 'LISTREEL'*NMOT;

    TABM = TABLE;
    REPETER BOUCM NMOT;
        TABM.(&BOUCM) = EXTR LCOMP &BOUCM;
    FIN BOUCM;

    REPE BOUC1 NBPART;

        NELE = DIME TABELE.(&BOUC1-1).ELE;
        REPE BOUC2 NELE;
            KEYi = TABELE.(&BOUC1-1).KEY.(&BOUC2-1);
            TABO.KEY = TABO.KEY ET (LECT KEYi);
            REPE BOUC3 NMOT;
                MOTi = TABM.&BOUC3;
                VALi = EXTR CHCONT MOTi &BOUC1 (&BOUC2-1) 1;
                TABO.MOTi = TABO.MOTi ET (PROG VALi);
            FIN BOUC3;
        FIN BOUC2;

    FIN BOUC1;
LIST TABO;
FINP TABO;

"""

    def jobdata(self):
        """Generate the content of the input fileself from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Return
        ------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""*** ------------------------
*** {self.problem.model.name}
*** ------------------------
***
*** {self.problem.model.description}
***
***
*** Author: {self.model.author}
*** Description: {self.model.description}
*** Date: {now}
*** Generated by:
***   compas_fea2 v{compas_fea2.__version__}
***   compas_fea2_castem v{compas_fea2_castem.__version__}
***
***------------------------------------------------------------------
***------------------------------------------------------------------
*** PROCEDURES FOR POST-TREATMENT
***------------------------------------------------------------------
***------------------------------------------------------------------

{self.procedures}

***------------------------------------------------------------------
***------------------------------------------------------------------
*** MODEL
***------------------------------------------------------------------
***------------------------------------------------------------------
***
{self.problem.model.jobdata()}
***
***
*** -----------------------------------------------------------------
*** -----------------------------------------------------------------
*** PROBLEM
*** -----------------------------------------------------------------
*** -----------------------------------------------------------------
***
{self.problem.jobdata()}
FIN;
"""
