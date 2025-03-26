from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import ReactionFieldResults
from compas_fea2.results import SectionForcesFieldResults


def dgibi_export_node_results(castem_tab3_input, list_compo, field_name, path):
    return f"""
N{castem_tab3_input} = DIME TAB3.{castem_tab3_input};
T{castem_tab3_input} = TAB3.{castem_tab3_input}.(N{castem_tab3_input}-1);
TAB{field_name} = CHPOTAB T{castem_tab3_input} (MOTS {list_compo}) TABPOINTS;
OPTI SORT '{path}\\{field_name}';
SORT 'EXCE' TAB{field_name} 'SEPA' 'ESPA';
"""


class CastemDisplacementFieldResults(DisplacementFieldResults):
    """"""

    __doc__ += DisplacementFieldResults.__doc__

    def __init__(self, **kwargs):
        super(CastemDisplacementFieldResults, self).__init__(**kwargs)

    def jobdata(self):
        castem_tab3_input = "DEPLACEMENTS"
        list_compo = "UX UY UZ RX RY RZ"
        return dgibi_export_node_results(castem_tab3_input, list_compo, self.field_name, self.problem.path)


class CastemReactionFieldResults(ReactionFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, **kwargs):
        super(CastemReactionFieldResults, self).__init__(**kwargs)

    def jobdata(self):
        castem_tab3_input = "REACTIONS"
        list_compo = "FX FY FZ MX MY MZ"
        return dgibi_export_node_results(castem_tab3_input, list_compo, self.field_name, self.problem.path)


class CastemSectionForcesFieldResults(SectionForcesFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, **kwargs):
        super(CastemSectionForcesFieldResults, self).__init__(**kwargs)

    def jobdata(self):
        return f"""
NCONTRAINTES = DIME TAB3.CONTRAINTES;
TCONTRAINTES = TAB3.CONTRAINTES.(NCONTRAINTES-1);
TAB{self.field_name} = SFTAB TCONTRAINTES TABELE;
OPTI SORT '{self.problem.path}\\{self.field_name}';
SORT  'EXCE' TAB{self.field_name} 'SEPA' 'ESPA';
"""
