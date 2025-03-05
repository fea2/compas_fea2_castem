from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import ConcentratedLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import HarmonicPointLoad
from compas_fea2.problem import HarmonicPressureLoad
from compas_fea2.problem import PressureLoad
from compas_fea2.problem import PrestressLoad
from compas_fea2.problem import TributaryLoad

dofs = ["x", "y", "z", "xx", "yy", "zz"]


class CastemConcentratedLoad(ConcentratedLoad):
    """Castem implementation of :class:`compas_fea2.problem.PointLoad`.\n"""

    __doc__ += ConcentratedLoad.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super(CastemConcentratedLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, **kwargs)

    def jobdata(self, node):
        castem_load= {"x": "FX", "y": "FY", "z": "FZ", "xx": "MX", "yy": "MY", "zz": "MZ"}
        load_dofs=[]
        for dof in dofs:
            if self.components[dof]:
                load_dofs.append(castem_load[dof]+' '+str(self.components[dof]))
        forc="FORC {0} N{1}".format(" ".join([load for load in load_dofs]), node.input_key )
        return """***
CHCHAR= {} ;
EVCHAR = CHAR 'MECA' CHCHAR EVOLC;
CHARTOT = CHARTOT ET EVCHAR;
""".format(forc)


class OpenseesPressureLoad(PressureLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.AreaLoad`.\n"""

    __doc__ += PressureLoad.__doc__

    def __init__(self, elements, x, y, z, axes, **kwargs):
        super(OpenseesPressureLoad, self).__init__(elements, x, y, z, axes, **kwargs)
        raise NotImplementedError


class OpenseesGravityLoad(GravityLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.GravityLoad`.\n"""

    __doc__ += GravityLoad.__doc__

    def __init__(self, g=9.81, x=0.0, y=0.0, z=-1.0, **kwargs):
        super(OpenseesGravityLoad, self).__init__(g, x, y, z, **kwargs)


class OpenseesPrestressLoad(PrestressLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PrestressLoad`.\n"""

    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes="global", **kwargs):
        super(OpenseesPrestressLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError


class OpenseesTributaryLoad(TributaryLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.TributaryLoad`.\n"""

    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes="global", **kwargs):
        super(OpenseesTributaryLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError
        # for v in self.model.discretized_boudary_mesh.vertices():
        #     n = self.model.find_node_by_location(self.model.discretized_boudary_mesh.vertex_coordinates(v))
        #     gravity_load = GravityLoad(g, x, y, z)
        #     tributary_area = self.model.discretized_boudary_mesh.vertex_area(v)
        #     tributary_volume = tributary_area


class OpenseesHarmonicPointLoad(HarmonicPointLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPointLoad`.\n"""

    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes="global", **kwargs):
        super(OpenseesHarmonicPointLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError


class OpenseesHarmonicPressureLoad(HarmonicPressureLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPressureLoad`.\n"""

    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes="global", **kwargs):
        super(OpenseesHarmonicPressureLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError
