from compas_fea2.model import BeamElement
from compas_fea2.model import LinkElement
from compas_fea2.model import ShellElement
from compas_fea2.model import TetrahedronElement
from compas_fea2.model import _Element3D


def jobdata(element):
    """Generates the list of information for the generation for the input file of all the
    elements.

    Note
    ----
    the string portion is generated in the part section
    to group elements with the same type.

    Parameters
    ----------
    None

    Returns
    -------
    List with input file data of the element (str).

    """
    return [element.key, " N".join(str(node.key) for node in element.nodes)]


# ==============================================================================
# 0D elements
# ==============================================================================
class CastemLinkElement(LinkElement):
    """Check the documentation \n
    https://www-cast3m.cea.fr/index.php?page=notices&notice=RELA#Option%20ENSE%20:%20relation%20de%20mouvement%20d'ensemble15

    The RELA operator returns a rigidity matrix corresponding to the linked movement. It will have to be integrated to
    the TAB3.RIGIDITE matrix.
    """

    __doc__ += LinkElement.__doc__

    def __init__(self, nodes, **kwargs):
        super(CastemLinkElement, self).__init__(nodes=nodes, **kwargs)

    def jobdata(self):
        return f""" 
LINK{self.key}X = RELA UX N{self.nodes[0].key} - UX N{self.nodes[-1].key};
LINK{self.key}Y = RELA UY N{self.nodes[0].key} - UY N{self.nodes[-1].key};
LINK{self.key}Z = RELA UZ N{self.nodes[0].key} - UZ N{self.nodes[-1].key};
LINK{self.key}RX = RELA RX N{self.nodes[0].key} - RX N{self.nodes[-1].key};
LINK{self.key}RY = RELA RY N{self.nodes[0].key} - RY N{self.nodes[-1].key};
LINK{self.key}RZ = RELA RZ N{self.nodes[0].key} - RZ N{self.nodes[-1].key};
LINK{self.key}TOT = LINK{self.key}X ET LINK{self.key}Y ET LINK{self.key}Z
ET LINK{self.key}RX ET LINK{self.key}RY ET LINK{self.key}RZ;

LINKTOT = LINKTOT ET LINK{self.key}TOT;
"""


# ==============================================================================
# 1D elements
# ==============================================================================
class CastemBeamElement(BeamElement):
    """Castem implementation of :class:`compas_fea2.model.BeamElement`.\n"""

    __doc__ += BeamElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    type : str, optional
        Name of the implementation model.
    
    type_element : str, optional
        Name of mess element

    Note
    ----
    Only 3d elements are implemented.
    The available implementations are listed below

        - SEG2
    Under development :
        - TIMO
        - BARR

    """

    def __init__(
        self,
        nodes,
        section,
        frame=[0.0, 0.0, -1.0],
        type="POUT",
        type_element="SEG2",
        implementation=None,
        **kwargs,
    ):
        super().__init__(
            nodes=nodes,
            section=section,
            frame=frame,
            implementation=implementation or str(type),
            **kwargs,
        )

        self._type_element = type_element  # type element de maillage
        self._type = type
        self._orientation = frame  # FIXME this is useless

    def jobdata(self):
        if any(x in self.implementation for x in ["POUT", "TIMO", "BARRE"]):
            return jobdata(self)
        else:
            raise NotImplementedError


# ==============================================================================
# 2D elements
# ==============================================================================


class CastemShellElement(ShellElement):
    """CASTEM implementation of a :class:`ShellElemnt`."""

    __doc__ += ShellElement.__doc__
    __doc__ += """

    Shell modelisation types :
    ---------------------
    COQ3 mode / TRI3 element :
        3-node triangular elements for thin shell with Kirchhoff-Love hypothesis.
    COQ4 mode / QUA4 element :
        4-node quadrangular elements for thin shell with shear.
    COQ6 mode / TRI6 element :
        6-node triangular element, thick shell with Mindlin-Reissner hypothesis
    COQ8 mode /QUA8 element :
        8-node quadrangular element, thick shell with Mindlin-Reissner hypothesis and curved sides
    DKT mode / TRI3 element :
        3-node triangular elements for thin shell (Discrete Kirchhoff Triangle)
    DST mode / TRI3 :
        3-node triangular elements for thick shell ( Discrete Shear Triangle)

    Notes
    -----
    The element's frame is set to have one axis parallel to the segment connecting the first
    and the second node and the third axis peperdicular to the plane of the element.

    """

    def __init__(self, nodes, section, implementation=None, **kwargs):
        super(CastemShellElement, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)
        if not self.implementation:
            if len(nodes) == 3:
                self._implementation = "COQ3"
                self._type_element = "TRI3"
            elif len(nodes) == 4:
                self._implementation = "COQ4"
                self._type_element = "QUA4"
            elif len(nodes) == 6:
                self._implementation = "COQ6"
                self._type_element = "TRI6"
            elif len(nodes) == 8:
                self._implementation = "COQ8"
                self._type_element = "QUA8"
            else:
                raise NotImplementedError("An element with {} nodes is not supported".format(len(nodes)))

    def jobdata(self):
        if any(x in self.implementation for x in ["COQ3", "COQ4", "COQ6", "COQ8", "DKT", "DST"]):
            return jobdata(self)
        else:
            raise NotImplementedError


# ==============================================================================
# 3D elements
# ==============================================================================


class _CastemElement3D(_Element3D):
    """CASTEM implementation of a :class:`_Element3D`."""

    __doc__ += _Element3D.__doc__

    def __init__(self, nodes, section, implementation=None, **kwargs):
        super(_CastemElement3D, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)
        if not self.implementation:
            self._implementation = "massif"
            if len(nodes) == 4:
                self._type_element = "TET4"
            elif len(nodes) == 5:
                self._type_element = "PYR5"
            elif len(nodes) == 6:
                self._type_element = "PRI6"
            elif len(nodes) == 8:
                self._type_element = "CUB8"
            elif len(nodes) == 10:
                self._type_element = "TE10"
            elif len(nodes) == 13:
                self._type_element = "PY13"
            elif len(nodes) == 15:
                self._type_element = "PY15"
            elif len(nodes) == 20:
                self._type_element = "CU20"
            else:
                raise NotImplementedError("An element with {} nodes is not supported".format(len(nodes)))

    def jobdata(self):
        if any(x in self._type_element for x in ["TET4", "PYR5", "PRI6", "CUB8", "TE10", "PY13", "PY15", "CU20"]):
            return jobdata(self)
        else:
            raise NotImplementedError


class CastemTetrahedronElement(TetrahedronElement, _CastemElement3D):
    """Castem implementation of :class:`TetrahedronElement`"""

    __doc__ += TetrahedronElement.__doc__

    def __init__(self, nodes, section=None, implementation=None, **kwargs):
        super(CastemTetrahedronElement, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)

    def jobdata(self):
        if any(x in self._type_element for x in ["TET4", "TE10"]):
            return jobdata(self)
        else:
            raise ValueError("A solid element with {} nodes cannot be created.".format(len(self.nodes)))
