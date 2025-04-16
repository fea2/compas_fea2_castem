from compas_fea2.problem import LoadCombination


class CastemLoadCombination(LoadCombination):
    """Castem implementation of :class:`compas_fea2.problem.LoadCombination`.\n"""

    __doc__ += LoadCombination.__doc__

    def __init__(self, factors, **kwargs):
        super().__init__(factors=factors, **kwargs)

    def jobdata(self):
        # implementation with LoadField
        # return ""
        return "\n".join([load.jobdata(node) for node, load in self.node_load])
