from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import AngleSection
from compas_fea2.model import BeamSection
from compas_fea2.model import BoxSection
from compas_fea2.model import CircularSection
from compas_fea2.model import HexSection
from compas_fea2.model import ISection
from compas_fea2.model import MassSection
from compas_fea2.model import MembraneSection
from compas_fea2.model import PipeSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import SolidSection
from compas_fea2.model import SpringSection
from compas_fea2.model import StrutSection
from compas_fea2.model import TieSection
from compas_fea2.model import TrapezoidalSection
from compas_fea2.model import TrussSection

# NOTE: these classes are sometimes overwriting the _base ones because Abaqus offers internal ways of computing beam sections' properties


def beam_jobdata(self):
    return "SECT {0} INRY {1} INRZ {2} TORS {3} SECY {4} SECZ{5}".format(self.A, self.Ixx, self.Iyy, self.J, self.Avx, self.Avy)


# ==============================================================================
# 0D
# ==============================================================================
class AbaqusMassSection(MassSection):
    """Abaqus implementation of the :class:`MassSection`.\n"""

    __doc__ += MassSection.__doc__

    def __init__(self, mass, name=None, **kwargs):
        super(AbaqusMassSection, self).__init__(mass, name=name, **kwargs)

    def jobdata(self, set_name):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** Section: \"{}\"
*Mass, elset={}
{}\n""".format(
            self.name, set_name, self.mass
        )


class AbaqusSpringSection(SpringSection):
    """Abaqus implementation of the :class:`SpringSection`.\n"""

    __doc__ += SpringSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, forces=None, displacements=None, stiffness=None, name=None, **kwargs):
        super().__init__(forces, displacements, stiffness, name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


# ==============================================================================
# 1D
# ==============================================================================


class AbaqusBeamSection(BeamSection):
    """Abaqus implementation of the :class:`BeamSection`.\n"""

    __doc__ += BeamSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, name=None, **kwargs):
        super().__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class CastemAngleSection(AngleSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += AngleSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, w, h, t, material, name=None, **kwargs):
        super(CastemAngleSection, self).__init__(w, h, t, material, name=name, **kwargs)

    def jobdata(self):
        return beam_jobdata(self)


class CastemBoxSection(BoxSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, t, material, **kwargs):
        super(CastemBoxSection, self).__init__(self, w, h, t, material, **kwargs)

    def jobdata(self):
        return beam_jobdata(self)


class CastemCircularSection(CircularSection):
    """Abaqus implementation of the :class:`CircularSection`.\n"""

    __doc__ += CircularSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, material, name=None, **kwargs):
        super(CastemCircularSection, self).__init__(r, material, name=name, **kwargs)
        self._properties = [r]

    def jobdata(self):
        return beam_jobdata(self)


class CastemHexSection(HexSection):
    """Abaqus implementation of the :class:`HexSection`.\n"""

    __doc__ += HexSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, t, material, name=None, **kwargs):
        super(CastemHexSection, self).__init__(r, t, material, name=name, **kwargs)
        self._stype = "hex"
        self.properties = [r, t]

    def jobdata(self):
        return beam_jobdata(self)


class CastemISection(ISection):
    """ """

    __doc__ += ISection.__doc__

    def __init__(self, w, h, tw, tbf, ttf, material, **kwargs):
        super(CastemISection, self).__init__(w, h, tw, tbf, ttf, material, **kwargs)

    def jobdata(self):
        return beam_jobdata(self)


class CastemPipeSection(PipeSection):
    """Abaqus implementation of the :class:`PipeSection`.\n"""

    __doc__ += PipeSection.__doc__

    # TODO Cast3m might have some complementary properties

    def __init__(self, r, t, material, name=None, **kwarg):
        super(CastemPipeSection, self).__init__(r, t, material, name=name, **kwarg)

    def jobdata(self):
        return beam_jobdata(self)


class CastemRectangularSection(RectangularSection):
    """Castem implementation of the :class:`RectangularSection`.\n"""

    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, name=None, **kwargs):
        super(CastemRectangularSection, self).__init__(w=w, h=h, material=material, name=name, **kwargs)

    def jobdata(self):
        return beam_jobdata(self)


class AbaqusTrapezoidalSection(TrapezoidalSection):
    """Abaqus implementation of the :class:`TrapezoidalSection`.\n"""

    __doc__ += TrapezoidalSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, w1, w2, h, material, name=None, **kwargs):
        super(AbaqusTrapezoidalSection, self).__init__(w1, w2, h, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


# TODO -> check how these sections are implemented in ABAQUS
class AbaqusTrussSection(TrussSection):
    """Abaqus implementation of the :class:`TrussSection`.\n"""

    __doc__ += TrussSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTrussSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class AbaqusStrutSection(StrutSection):
    """Abaqus implementation of the :class:`StrutSection`.\n"""

    __doc__ += StrutSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusStrutSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{self.__class__.__name__} is not available in Abaqus")


class AbaqusTieSection(TieSection):
    """Abaqus implementation of the :class:`TieSection`.\n"""

    __doc__ += TieSection.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, A, material, name=None, **kwargs):
        super(AbaqusTieSection, self).__init__(A, material, name=name, **kwargs)
        raise NotImplementedError("{} is not available in Abaqus".format(TieSection.__name__))


# ==============================================================================
# 2D
# ==============================================================================


class CastemShellSection(ShellSection):
    """Abaqus implementation of the :class:`ShellSection`.\n"""

    __doc__ += ShellSection.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    int_points : int
        number of integration points. 5 by default.
    """

    def __init__(self, t, material, int_points=5, name=None, **kwargs):
        super(CastemShellSection, self).__init__(t, material, name=name, **kwargs)
        self.int_points = int_points

    def jobdata(self, **kwargs):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return f"EPAI {self.t}"


class CastemMembraneSection(MembraneSection):
    """Abaqus implementation of the :class:`MembraneSection`.\n"""

    __doc__ += MembraneSection.__doc__

    def __init__(self, t, material, name=None, **kwargs):
        super(CastemMembraneSection, self).__init__(t, material, name=name, **kwargs)

    def jobdata(self, set_name, **kwargs):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        raise NotImplementedError("{} is not available in Abaqus".format(MembraneSection.__name__))


# ==============================================================================
# 3D
# ==============================================================================


class CastemSolidSection(SolidSection):
    """Abaqus implementation of the :class:`SolidSection`.\n"""

    __doc__ += SolidSection.__doc__

    def __init__(self, material, name=None, **kwargs):
        super(CastemSolidSection, self).__init__(material, name=name, **kwargs)

    def jobdata(self, **kwargs):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        pass
