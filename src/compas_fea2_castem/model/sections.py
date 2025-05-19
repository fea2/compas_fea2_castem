from compas_fea2.model import AngleSection
from compas_fea2.model import BoxSection
from compas_fea2.model import CircularSection
from compas_fea2.model import HexSection
from compas_fea2.model import ISection
from compas_fea2.model import PipeSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import SolidSection


def _beam_jobdata(self):
    """In Castem, the strong axis of inertia of the section is axis Y and the "weak" one is axis Z."""
    return f"SECT {self.A} INRY {self.Ixx} INRZ {self.Iyy} TORS {self.J} SECY {self.Avy} SECZ {self.Avx}"


# ==============================================================================
# 0D
# ==============================================================================


# ==============================================================================
# 1D
# ==============================================================================
class CastemAngleSection(AngleSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += AngleSection.__doc__

    def __init__(self, w, h, t, material, **kwargs):
        super().__init__(w, h, t, material, **kwargs)

    def jobdata(self):
        return _beam_jobdata(self)


class CastemBoxSection(BoxSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, t, material, **kwargs):
        super().__init__(self, w, h, t, material, **kwargs)

    def jobdata(self):
        return _beam_jobdata(self)


class CastemCircularSection(CircularSection):
    """Castem implementation of the :class:`CircularSection`.\n"""

    __doc__ += CircularSection.__doc__

    def __init__(self, r, material, **kwargs):
        super().__init__(r, material, **kwargs)
        self._properties = [r]

    def jobdata(self):
        return _beam_jobdata(self)


class CastemHexSection(HexSection):
    """Castem implementation of the :class:`HexSection`.\n"""

    __doc__ += HexSection.__doc__

    def __init__(self, r, t, material, **kwargs):
        super().__init__(r, t, material, **kwargs)
        self._stype = "hex"
        self.properties = [r, t]

    def jobdata(self):
        return _beam_jobdata(self)


class CastemISection(ISection):
    """Castem implementation of the :class:`ISection`. \n"""

    __doc__ += ISection.__doc__

    def __init__(self, w, h, tw, tbf, ttf, material, **kwargs):
        super().__init__(w, h, tw, tbf, ttf, material, **kwargs)

    def jobdata(self):
        return _beam_jobdata(self)


class CastemPipeSection(PipeSection):
    """Castem implementation of the :class:`PipeSection`.\n"""

    __doc__ += PipeSection.__doc__

    # TODO Cast3m might have some complementary properties

    def __init__(self, r, t, material, **kwarg):
        super().__init__(r, t, material, **kwarg)

    def jobdata(self):
        return _beam_jobdata(self)


class CastemRectangularSection(RectangularSection):
    """Castem implementation of the :class:`RectangularSection`.\n"""

    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, **kwargs):
        super().__init__(w=w, h=h, material=material, **kwargs)

    def jobdata(self):
        return _beam_jobdata(self)


# ==============================================================================
# 2D
# ==============================================================================
class CastemShellSection(ShellSection):
    """Castem implementation of the :class:`ShellSection`.\n"""

    __doc__ += ShellSection.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    int_points : int
        number of integration points. 5 by default.
    """

    def __init__(self, t, material, int_points=5, **kwargs):
        super().__init__(t, material, **kwargs)
        self.int_points = int_points

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return f"EPAI {self.t}"


# ==============================================================================
# 3D
# ==============================================================================
class CastemSolidSection(SolidSection):
    """Castem implementation of the :class:`SolidSection`.
    No specific parameters are needed in a solid model.\n"""

    __doc__ += SolidSection.__doc__

    def __init__(self, material, **kwargs):
        super().__init__(material, **kwargs)

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        """
        return None
