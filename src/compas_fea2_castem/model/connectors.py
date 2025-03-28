from compas_fea2.model import RigidLinkConnector


class CastemRigidLinkConnector(RigidLinkConnector):
    """Castem implementation of :class:`compas_fea2.model.connectors.RigidLinkConnector`."""

    __doc__ += RigidLinkConnector.__doc__

    def __init__(self, nodes, dofs="beam", **kwargs):
        super().__init__(nodes, dofs, **kwargs)

    def jobdata(self):
        castem_dofs = {1: "UX", 2: "UY", 3: "UZ", 4: "RX", 5: "RY", 6: "RZ"}
        # FIXME: beam and bar have the same DOFs
        dof_map = {
            "beam": [1, 2, 3],
            "bar": [1, 2, 3],
        }
        fea2_dofs = dof_map.get(self.dofs, self.dofs)
        cNode = self.nodes[0].key
        rNode = self.nodes[1].key
        return "\n".join(f"CONTOT = CONTOT ET (RELA 1 {castem_dofs[dof]} N{rNode} - 1 {castem_dofs[dof]} N{cNode});" for dof in fea2_dofs)
