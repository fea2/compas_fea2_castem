from compas_fea2.problem import ConcentratedLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import PressureLoad

dofs = ["x", "y", "z", "xx", "yy", "zz"]


class CastemConcentratedLoad(ConcentratedLoad):
    """Castem implementation of :class:`compas_fea2.problem.PointLoad`.

    https://www-cast3m.cea.fr/index.php?page=notices&notice=CHAR


    \n"""

    __doc__ += ConcentratedLoad.__doc__

    __doc__ += """
    The CHAR operator creates a CHARGEMENT (loading) object that associates a loading field to
    a temporal evolution, necessary to the implementation of PASAPAS procedure.
    The temporal evolution can be impactful in a non-linear analysis.

    WARNING
    -----------
    The jobdata implementation of punctual loads is not used anymore for the generation of the input file.
    All is done in the Loadfields classes.

 """

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super().__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, **kwargs)

    def jobdata(self, node):
        castem_load = {
            "x": "FX",
            "y": "FY",
            "z": "FZ",
            "xx": "MX",
            "yy": "MY",
            "zz": "MZ",
        }
        load_dofs = []
        for dof in dofs:
            if self.components[dof]:
                load_dofs.append(castem_load[dof] + " " + str(self.components[dof]))
        forc = "FORC {0} N{1}".format(" ".join([load for load in load_dofs]), node.key)
        return f"""***
CHCHAR= {forc} ;
EVCHAR = CHAR 'MECA' CHCHAR EVOLC;
CHARTOT = CHARTOT ET EVCHAR;
"""


class CastemPressureLoad(PressureLoad):
    """Castem implementation of :class:`compas_fea2.problem.PressureLoad`.\n"""

    __doc__ += PressureLoad.__doc__

    __doc__ += """
    The CHAR operator creates a CHARGEMENT (loading) object that associates a loading field to
    a temporal evolution, necessary to the implementation of PASAPAS procedure.
    The temporal evolution can be impactful in a non-linear analysis.
 """

    def __init__(self, elements, x=0, y=0, z=0, axes="local", **kwargs):
        super().__init__(elements=elements, x=x, y=y, z=z, axes=axes, **kwargs)

    def jobdata(self):
        # creation of the point field containing the loaded elements
        # first the elements are sorted by implementation
        implementations = set(map(lambda x: x._implementation, self.elements))
        grouped_elements = {implementation: [el for el in self.elements if el._implementation == implementation] for implementation in implementations}

        # Castem implementation of the element field (MCHAML type)
        # the PRES procedure needs to differenciate the COQ elements from massive elements

        presload_data = []
        presload_data.append(f"MAILPRES{self._registration} = VIDE 'MAILLAGE';")
        for implementation, elements in grouped_elements.items():
            # shell elements
            if implementation in ["COQ3", "COQ4", "COQ6", "COQ8", "DKT", "DST"]:
                PRESS_type = "COQU"

            elif implementation in ["TET4", "PYR5", "PRI6", "CUB8", "TE10", "PY13", "PY15", "CU20"]:
                PRESS_type = "MASS"

            else:
                raise ValueError("Some elements are not eligible for the pressure load procedure (only shell or massive elements accepted).")
            mail_data = f"MPRES{PRESS_type[0]}{self._registration} = "

            first = True
            for element in elements:
                # castem does not accept lines that are too long, we limit the length of a line to 24 characters
                if (len(mail_data) + 4 + len(element.key)) > 24:
                    presload_data.append(mail_data)
                    mail_data = ""

                if first:
                    mail_data += f"E{element.key} "
                    first = False
                else:
                    mail_data += f"ET E{element.key}"

            presload_data.append(mail_data)

        return "\n".join(presload_data)


class CastemGravityLoad(GravityLoad):
    """Castem implementation of :class:`compas_fea2.problem.GravityLoad`.\n
    The gravity load is applied on the whole mesh.
    The CHAR operator creates a CHARGEMENT object that associates a loading field to
    a temporal evolution, necessary to the implementation of PASAPAS procedure.
    In compas_fea2_castem implementation, the temporal evolution is not meaningfully implemented.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=MASS
    https://www-cast3m.cea.fr/index.php?page=notices&notice=CHAR

    """

    __doc__ += GravityLoad.__doc__

    def __init__(self, g=9.81, x=0.0, y=0.0, z=-1.0, **kwargs):
        super().__init__(g=g, x=x, y=y, z=z, **kwargs)

    def jobdata(self, *args, **kwargs):
        return f"""
*Mass matrix of the complete model
MASTOT = MASS MODTOT MATOT;
*Acceleration field applied on the total mesh
ACCGP = MANU CHPO MAILTOT 1 UZ {self.z + self.g} NATU DIFF;
GP = MASTOT * ACCGP;
*Load object created, associated to a temporal evolution
CHPP = CHAR 'MECA' GP EVOLC;
CHARTOT = CHARTOT ET CHPP;
"""
