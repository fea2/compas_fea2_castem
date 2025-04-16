from compas_fea2.model import Node


class CastemNode(Node):
    """Castem implementation of the :class:`Node`.

    https://www-cast3m.cea.fr/index.php?page=notices&notice=POIN

    The name of Cast3M objects must begin with a letter, hence the N letter.


    \n"""

    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, **kwargs):
        super().__init__(xyz=xyz, mass=mass, **kwargs)

    def jobdata(self):
        # FIXME: the approximation on the floating point is not correct
        # because it depends on the units
        x, y, z = self.xyz
        coordinates = "{0}{1}{2}{4:>15.8f}{3}{5:>15.8f}{3}{6:>15.8f}{7}".format("N", self.key, " = ", " ", x, y, z, ";")
        tabpoints_data = f"""
ID = DIME TABPOINTS.KEY;
TABPOINTS.KEY.ID = {self.key};
TABPOINTS.POINT.ID = N{self.key};
"""
        return coordinates + tabpoints_data  # + mass
