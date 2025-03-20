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
        super(CastemModel, self).__init__(description=description, author=author, **kwargs)

    def jobdata(self):
        return """***
*** By default, models in compas_fea2 are defined in 3D.
OPTI DIME 3;
***
***==================================================================
*** Parts & Material & Section
***==================================================================
***
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

***
***""".format(
            "\n".join([part.jobdata() for part in sorted(self.parts, key=lambda x: x.key)]),
            # "\n".join([material.jobdata() for material in sorted(self.materials, key=lambda x: x.key)]),
            # "\n".join([section.jobdata() for section in sorted(self.sections, key=lambda x: x.key) if not isinstance(section, (SolidSection, TrussSection))]),
            "\n".join([bc.jobdata(nodes) for bc, nodes in self.bcs.items()]),
            #            "\n".join([connector.jobdata() for connector in sorted(self.connectors, key=lambda x: x.key)]),
        )
