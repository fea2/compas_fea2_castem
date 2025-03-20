from compas_fea2.results import DisplacementFieldResults


def dgibi_export_node_results(tab_text, field_name, path):
    return f"""
{tab_text}
OPTI SORT '{path}\\{field_name}';
SORT 'AVS' CHP{field_name};
"""


class CastemDisplacementFieldResults(DisplacementFieldResults):
    """"""

    __doc__ += DisplacementFieldResults.__doc__

    def __init__(self, **kwargs):
        super(CastemDisplacementFieldResults, self).__init__(**kwargs)

    def jobdata(self):
        tab_text = """
N = DIME TAB3.DEPLACEMENTS;
TDEP = TAB3.DEPLACEMENTS.(N-1);
CHPu = EXCO (MOTS 'UX' 'UY' 'UZ' 'RX' 'RY' 'RZ')  TDEP;
"""
        return dgibi_export_node_results(tab_text, self.field_name, self.problem.path)
