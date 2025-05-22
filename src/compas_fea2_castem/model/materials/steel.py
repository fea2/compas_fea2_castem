from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Steel
from .material import CastemElasticIsotropic


def jobdata(mod, mate, parameters):
    return [mod, mate, parameters]


# ==============================================================================
# non-linear metal
# ==============================================================================


# class CastemSteel(Steel):
#     """"""

#     __doc__ += Steel.__doc__
#     __doc__ += """
#     Nota CASTEM
#     -----------
#     The elasto-plastic model used is isotrop with cinematic hardening.
#     https://www-cast3m.cea.fr/index.php?page=notices&notice=mate#MECANIQUE%20ELASTO-PLASTIQUE16
    
#     """

#     def __init__(self, *, fy, fu, eu, E, v, density, **kwargs):
#         super(CastemSteel, self).__init__(fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, **kwargs)
#         self._H = (self.fu - self.fy) / self.ep
#         self.mod = "MECANIQUE ELASTIQUE PLASTIQUE CINEMATIQUE"
#         self.mate = f"'YOUN' {self.E} 'NU' {self.v} 'RHO' {self.density} SIGY {fy} H {self.H} "
#         self.complementary_line = None

#     @property
#     def H(self):
#         return self._H

#     def jobdata(self):
#         return jobdata(self.mod, self.mate, self.complementary_line)

class CastemSteel(Steel, CastemElasticIsotropic):
    
    """"""

    __doc__ += Steel.__doc__
    __doc__ += """
    Nota CASTEM
    -----------
    The elasto-plastic model used is isotrop with cinematic hardening.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=mate#MECANIQUE%20ELASTO-PLASTIQUE16
    
    """

    def __init__(self, *, fy, fu, eu, E, v, density, **kwargs):
        super(CastemSteel, self).__init__(fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, **kwargs)
