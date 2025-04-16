from compas_fea2.model import Model


class CastemModel(Model):
    """Cast3m implementation of the :class::`Model`.

    For detailed information about Cast3m and its API, visit: https://www-cast3m.cea.fr/index.php

    Warning
    -------
    Work in Progress!

    General Objects
    -------

    TABPOINTS : Table
        > TABPOINTS.KEY.i : Key of Castem node number i
        > TABPOINTS.POINT.i : Correponding point of Castem node number i
    Aims at keeping track of the KEY number related to the node.
    Indeed, the CASTEM node number is relative to its order of creation. This is indicated by the ID element.

    TABELE : Table
        > TABELE.KEY.i : Key of Castem elements number i
        > TABELE.POINT.i : Correponding element of Castem element number i
    Aims at keeping track of the KEY number related to the element.
    Indeed, the CASTEM node number is relative to its order of creation. This is indicated by the ID element.

    MODTOT : MMODEL type
    All the models relatives to parts

    MODJTOT : MMODEL type
    All the models relatives to the joint

    MATTOT : MCHAML type
    All the material relatives to parts

    MATJTOT : MCHAML type
    All the material relatives to parts

    MAILTOT : MAILLAGE (mesh) type
    All the meshes.

    CRIGTOT : RIGIDITE (stiffness) type
    All criteria about rigid movement

    CLTOT : RIGIDITE (stiffness) type
    All criteria about boundary counditions and displacement conditions

    CONTOT : RIGIDITE (stiffness) type
    All criteria about connection between parts

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

*** Initialization of objects used later for the analysis

MODTOT = VIDE 'MMODEL';
MODJTOT = VIDE 'MMODEL';
MATTOT = VIDE 'MCHAML';
MATJTOT = VIDE 'MCHAML';
MAILTOT = VIDE 'MAILLAGE';

TABPOINTS = TABLE ;
TABPOINTS.KEY = TABLE;
TABPOINTS.POINT = TABLE;

TABELE = TABLE;

CRIGTOT = VIDE 'RIGIDITE'/'RIGIDITE';

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
*** Interaction and interfaces
***------------------------------------------------------------------
***
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
            "\n".join([interfaces.jobdata() for interfaces in sorted(self.interfaces, key=lambda x: x.key)]),
            "\n".join([connector.jobdata() for connector in sorted(self.connectors, key=lambda x: x.key)]),
        )
