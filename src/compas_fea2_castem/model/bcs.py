from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import ClampBCXX
from compas_fea2.model import ClampBCYY
from compas_fea2.model import ClampBCZZ
from compas_fea2.model import FixedBC
from compas_fea2.model import FixedBCX
from compas_fea2.model import FixedBCY
from compas_fea2.model import FixedBCZ
from compas_fea2.model import GeneralBC
from compas_fea2.model import PinnedBC
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCXZ
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCZ

dofs = ["x", "y", "z", "xx", "yy", "zz"]


def _jobdata(bc, nodes):
    castem_dofs = {"x": "UX", "y": "UY", "z": "UZ", "xx": "RX", "yy": "RY", "zz": "RZ"}
    mdl_dofs = []
    for dof in dofs:
        if getattr(bc, dof):
            mdl_dofs.append(castem_dofs[dof])

    return "\n".join(["CLTOT= CLTOT ET (BLOQ {0} N{1}) ;".format(" ".join([castem_dof for castem_dof in mdl_dofs]), node.key) for node in nodes])


class CastemGeneralBC(GeneralBC):
    """Castem implementation of :class:`compas_fea2.model.GeneralBC`.\n"""

    __doc__ += GeneralBC.__doc__

    def __init__(self, **kwargs):
        super(CastemGeneralBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBC(FixedBC):
    """Castem implementation of :class:`compas_fea2.model.FixedBC`.\n"""

    __doc__ += FixedBC.__doc__

    def __init__(self, **kwargs):
        super(CastemFixedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCX(FixedBCX):
    """Castem implementation of :class:`compas_fea2.model.FixedBCX`.\n"""

    __doc__ += FixedBCX.__doc__

    def __init__(self, **kwargs):
        super(CastemFixedBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCY(FixedBCY):
    """Castem implementation of :class:`compas_fea2.model.FixedBCY`.\n"""

    __doc__ += FixedBCY.__doc__

    def __init__(self, **kwargs):
        super(CastemFixedBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCZ(FixedBCZ):
    """Castem implementation of :class:`compas_fea2.model.FixedBCZ`.\n"""

    __doc__ += FixedBCZ.__doc__

    def __init__(self, **kwargs):
        super(CastemFixedBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemPinnedBC(PinnedBC):
    """Castem implementation of :class:`compas_fea2.model.PinnedBC`.\n"""

    __doc__ += PinnedBC.__doc__

    def __init__(self, **kwargs):
        super(CastemPinnedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCXX(ClampBCXX):
    """Castem implementation of :class:`compas_fea2.model.ClampBCXX`.\n"""

    __doc__ += ClampBCXX.__doc__

    def __init__(self, **kwargs):
        super(CastemClampBCXX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCYY(ClampBCYY):
    """Castem implementation of :class:`compas_fea2.model.ClampBCYY`.\n"""

    __doc__ += ClampBCYY.__doc__

    def __init__(self, **kwargs):
        super(CastemClampBCYY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCZZ(ClampBCZZ):
    """Castem implementation of :class:`ClampBCZZ`.\n"""

    __doc__ += ClampBCZZ.__doc__

    def __init__(self, **kwargs):
        super(CastemClampBCZZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCX(RollerBCX):
    """Castem implementation of :class:`RollerBCX`.\n"""

    __doc__ += RollerBCX.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCY(RollerBCY):
    """Castem implementation of :class:`RollerBCY`.\n"""

    __doc__ += RollerBCY.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCZ(RollerBCZ):
    """Castem implementation of :class:`RollerBCZ`.\n"""

    __doc__ += RollerBCZ.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCXY(RollerBCXY):
    """Castem implementation of :class:`RollerBCXY`.\n"""

    __doc__ += RollerBCXY.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCXY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCYZ(RollerBCYZ):
    """Castem implementation of :class:`RollerBCYZ`.\n"""

    __doc__ += RollerBCYZ.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCYZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCXZ(RollerBCXZ):
    """Castem implementation of :class:`RollerBCXZ`.\n"""

    __doc__ += RollerBCXZ.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCXZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)
