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
    active_dofs = [castem_dofs[dof] for dof in dofs if getattr(bc, dof)]
    dof_string = " ".join(active_dofs)
    return "\n".join(f"CLTOT= CLTOT ET (BLOQ {dof_string} N{node.key}) ;" for node in nodes)


class CastemGeneralBC(GeneralBC):
    """Castem implementation of :class:`compas_fea2.model.GeneralBC`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ

    \n"""

    __doc__ += GeneralBC.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBC(FixedBC):
    """Castem implementation of :class:`compas_fea2.model.FixedBC`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += FixedBC.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCX(FixedBCX):
    """Castem implementation of :class:`compas_fea2.model.FixedBCX`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += FixedBCX.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCY(FixedBCY):
    """Castem implementation of :class:`compas_fea2.model.FixedBCY`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += FixedBCY.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemFixedBCZ(FixedBCZ):
    """Castem implementation of :class:`compas_fea2.model.FixedBCZ`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += FixedBCZ.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemPinnedBC(PinnedBC):
    """Castem implementation of :class:`compas_fea2.model.PinnedBC`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += PinnedBC.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCXX(ClampBCXX):
    """Castem implementation of :class:`compas_fea2.model.ClampBCXX`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += ClampBCXX.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCYY(ClampBCYY):
    """Castem implementation of :class:`compas_fea2.model.ClampBCYY`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += ClampBCYY.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemClampBCZZ(ClampBCZZ):
    """Castem implementation of :class:`ClampBCZZ`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += ClampBCZZ.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCX(RollerBCX):
    """Castem implementation of :class:`RollerBCX`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCX.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCY(RollerBCY):
    """Castem implementation of :class:`RollerBCY`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCY.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCZ(RollerBCZ):
    """Castem implementation of :class:`RollerBCZ`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCZ.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCXY(RollerBCXY):
    """Castem implementation of :class:`RollerBCXY`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCXY.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCYZ(RollerBCYZ):
    """Castem implementation of :class:`RollerBCYZ`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCYZ.__doc__

    def __init__(self, **kwargs):
        super(CastemRollerBCYZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class CastemRollerBCXZ(RollerBCXZ):
    """Castem implementation of :class:`RollerBCXZ`.

    The BLOQ operator is used.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=BLOQ
    \n"""

    __doc__ += RollerBCXZ.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)
