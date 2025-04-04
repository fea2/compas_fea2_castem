from compas_fea2.model import Model


class CastemModel(Model):
    """Cast3m implementation of the :class::`Model`.

    For detailed information about Cast3m and its API visit: https://www-cast3m.cea.fr/index.php

    Warning
    -------
    Work in Progress!

    """

    __doc__ += Model.__doc__

    def __init__(self, description=None, author=None, **kwargs):
        super().__init__(description=description, author=author, **kwargs)

    def jobdata(self):
        return """***
*** By default, models in compas_fea2 are defined in 3D.
OPTI DIME 3;
***
***==================================================================
*** Parts & Material & Section
***==================================================================
***

*** Initialization of "stocking" object used for the analysis

MODTOT = VIDE 'MMODEL';
MATTOT = VIDE 'MCHAML';
MAILTOT = VIDE 'MAILLAGE';

TABPOINTS = TABLE ;
TABPOINTS.KEY = TABLE;
TABPOINTS.POINT = TABLE;

TABELE = TABLE;

{}
***
***
***------------------------------------------------------------------
*** Initial conditions
***------------------------------------------------------------------
***
CLTOT = VIDE 'RIGIDITE'/'RIGIDITE';
{}
***
***
***------------------------------------------------------------------
*** Connectors
***------------------------------------------------------------------
***
CONTOT = VIDE 'RIGIDITE'/'RIGIDITE';
{}
***
***""".format(
            "\n".join([part.jobdata() for part in sorted(self.parts, key=lambda x: x.key)]),
            "\n".join([bc.jobdata(nodes) for bc, nodes in self.bcs.items()]),
            "\n".join([connector.jobdata() for connector in sorted(self.connectors, key=lambda x: x.key)]),
        )
