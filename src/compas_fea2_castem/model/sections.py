from compas_fea2.model import AngleSection
from compas_fea2.model import BoxSection
from compas_fea2.model import CircularSection
from compas_fea2.model import HexSection
from compas_fea2.model import ISection
from compas_fea2.model import PipeSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import SolidSection


def _jobdata(self):
    return "SECT {0} INRY {1} INRZ {2} TORS {3} SECY {4} SECZ{5}".format(self.A, self.Ixx, self.Iyy, self.J, self.Avx, self.Avy)


# ==============================================================================
# 0D
# ==============================================================================


# ==============================================================================
# 1D
# ==============================================================================
class CastemAngleSection(AngleSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += AngleSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, w, h, t, material, **kwargs):
        super().__init__(w, h, t, material, **kwargs)

    def jobdata(self):
        return _jobdata(self)


class CastemBoxSection(BoxSection):
    """Castem implementation of the :class:`BoxSection`.\n"""

    __doc__ += BoxSection.__doc__

    def __init__(self, w, h, t, material, **kwargs):
        super().__init__(self, w, h, t, material, **kwargs)

    def jobdata(self):
        return _jobdata(self)


class CastemCircularSection(CircularSection):
    """Abaqus implementation of the :class:`CircularSection`.\n"""

    __doc__ += CircularSection.__doc__
    __doc__ += """
    Note
    ----
    The section properties are automatically computed by Abaqus.

    """

    def __init__(self, r, material, **kwargs):
        super().__init__(r, material, **kwargs)
        self._properties = [r]

    def jobdata(self):
        return _jobdata(self)


class CastemHexSection(HexSection):
    """Abaqus implementation of the :class:`HexSection`.\n"""

    __doc__ += HexSection.__doc__

    def __init__(self, r, t, material, **kwargs):
        super().__init__(r, t, material, **kwargs)
        self._stype = "hex"
        self.properties = [r, t]

    def jobdata(self):
        return _jobdata(self)


class CastemISection(ISection):
    """ """

    __doc__ += ISection.__doc__

    def __init__(self, w, h, tw, tbf, ttf, material, **kwargs):
        super().__init__(w, h, tw, tbf, ttf, material, **kwargs)

    def jobdata(self):
        return _jobdata(self)


class CastemPipeSection(PipeSection):
    """Abaqus implementation of the :class:`PipeSection`.\n"""

    __doc__ += PipeSection.__doc__

    # TODO Cast3m might have some complementary properties

    def __init__(self, r, t, material, **kwarg):
        super().__init__(r, t, material, **kwarg)

    def jobdata(self):
        return _jobdata(self)


class CastemRectangularSection(RectangularSection):
    """Castem implementation of the :class:`RectangularSection`.\n"""

    __doc__ += RectangularSection.__doc__

    def __init__(self, w, h, material, **kwargs):
        super().__init__(w=w, h=h, material=material, **kwargs)

    def jobdata(self):
        return _jobdata(self)


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
    """Abaqus implementation of the :class:`SolidSection`.\n"""

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
        input file data line (str).
        """
        pass
