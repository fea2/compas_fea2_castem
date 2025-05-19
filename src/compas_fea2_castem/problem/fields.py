from compas_fea2.problem import DisplacementField

# from compas_fea2.problem import GravityLoadField
from compas_fea2.problem import NodeLoadField

dofs = ["x", "y", "z", "xx", "yy", "zz"]


class CastemNodeLoadField(NodeLoadField):
    """Castem implementation of :class:`NodeLoadField`\n"""

    __doc__ += NodeLoadField.__doc__

    """ """

    def __init__(self, loads, nodes, load_case=None, **kwargs):
        super().__init__(loads, nodes, load_case, **kwargs)

    def castem_nodeload_input(self, node, loads):
        castem_load = {"x": "FX", "y": "FY", "z": "FZ", "xx": "MX", "yy": "MY", "zz": "MZ"}

        return f""" 
CHCHAR = FORC {" ".join([(castem_load[dof] + " " + str(loads.components[dof]) if loads.components[dof] else "") for dof in dofs])} {node.key};
EVCHAR = CHAR 'MECA' CHCHAR EVOLC;
CHARTOT = CHARTOT ET EVCHAR;
"""

    def jobdata(self):
        return "\n".join([self.castem_nodeload_input(node=node_load[0], loads=node_load[1]) for node_load in list(self.node_load)])


class CastemDisplacementField(DisplacementField):
    def __init__(self, displacements, nodes, load_case=None, **kwargs):
        super().__init__(displacements, nodes, load_case, **kwargs)

    def castem_imposeddisp_input(self, node, displacement, dof):
        castem_dofs = {"x": "UX", "y": "UY", "z": "UZ", "xx": "RX", "yy": "RY", "zz": "RZ"}
        if getattr(displacement, dof):
            return f"""CLDEP{dof}{node.key} = BLOQ N{node.key} {castem_dofs.get(dof)};
CLTOT = CLTOT ET CLDEP{dof}{node.key};
DEPL{dof}{node.key} = DEPI CLDEP{dof}{node.key} {getattr(displacement, dof)};
CHDEP{dof}{node.key} = CHAR 'DIMP' DEPL{dof}{node.key} EVOLC;
CHARTOT = CHARTOT ET CHDEP{dof}{node.key};

"""

    def jobdata(self):
        data = [self.castem_imposeddisp_input(node, displacement, dof) for dof in dofs for (node, displacement) in self.node_displacement]
        return "\n".join(["\n".join(line for line in data if line is not None)])


# class CastemGravityLoadField(GravityLoadField):
#     def __init__(self, g=9.81, parts=None, load_case=None, **kwargs):
#         super().__init__(g, parts, load_case, **kwargs)

#     def castem_gravity_input(self, part):
#         return f"""MAS{part.key} = MOD{part.key} MAT{self.key};
# ACC{part.key} = MANU CHPO MAIL{part.key} 1 UZ {self.g} NATU DIFF;
# GP{part.key} = MAS{part.key} * ACC{part.key};
# CHSW{part.key} = CHAR 'MECA' GP{part.key} EVOLC;
# CHARTOT = CHARTOT ET CHSW{part.key};
# """

#     def jobdata(self):
#         return "\n".join([self.castem_gravity_input(part) for part in self.parts])
