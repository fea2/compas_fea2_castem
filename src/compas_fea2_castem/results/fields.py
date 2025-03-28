import os

from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import ReactionFieldResults
from compas_fea2.results import SectionForcesFieldResults
from compas_fea2.results import StressFieldResults


def _dgibi_export_node_results(castem_tab3_input, list_compo, field_name, path):
    return f"""
N{castem_tab3_input} = DIME TAB3.{castem_tab3_input};
T{castem_tab3_input} = TAB3.{castem_tab3_input}.(N{castem_tab3_input}-1);
TAB{field_name} = CHPOTAB T{castem_tab3_input} (MOTS {list_compo}) TABPOINTS;
OPTI SORT '{path}\\{field_name}';
SORT 'EXCE' TAB{field_name} 'SEPA' 'ESPA';
"""


def _extract_results(obj):
    """
    Read the .out results file and convert it to a dictionary.

    Parameters
    ----------
    database_path : path
        Path to the folder where the sqlite database will be created
    database_name : str
        Name of the database
    field_output : :class:`compas_fea2.problem.FieldOutput`
        FieldOutput object containing the nodes and/or element outputs to extract.
    """

    results = []
    with open(os.path.join(obj.problem_path, f"{obj.field_name}.csv"), "r") as f:
        # remove the first line of names of columns
        lines = f.readlines()[1:]
        for line in lines:
            columns = line.split()
            input_key = int(columns[0])  # Convert the first column to int
            member = getattr(obj.model, obj.field_output.results_func)(input_key)[0]
            values = list(map(lambda x: round(float(x), 6), columns[1:]))
            if not values:
                continue

            if len(values) < len(obj.field_output.components_names):
                values = values + [0.0] * (len(obj.field_output.components_names) - len(values))
            elif len(values) > len(obj.field_output.components_names):
                values = values[: len(obj.field_output.components_names)]
            else:
                values = values

            results.append([member.key] + [obj.step.name, member.part.name] + values)

    obj.field_output.create_sql_table(results)


class CastemDisplacementFieldResults(DisplacementFieldResults):
    """"""

    __doc__ += DisplacementFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        castem_tab3_input = "DEPLACEMENTS"
        list_compo = "UX UY UZ RX RY RZ"
        return _dgibi_export_node_results(castem_tab3_input, list_compo, self.field_name, self.problem.path)

    def extract_results(self):
        _extract_results(self)


class CastemReactionFieldResults(ReactionFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        castem_tab3_input = "REACTIONS"
        list_compo = "FX FY FZ MX MY MZ"
        return _dgibi_export_node_results(castem_tab3_input, list_compo, self.field_name, self.problem.path)

    def extract_results(self):
        _extract_results(self)


class CastemSectionForcesFieldResults(SectionForcesFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        return f"""
NCONTRAINTES = DIME TAB3.CONTRAINTES;
TCONTRAINTES = TAB3.CONTRAINTES.(NCONTRAINTES-1);
TAB{self.field_name} = SFTAB TCONTRAINTES TABELE;
OPTI SORT '{self.problem.path}\\{self.field_name}';
SORT  'EXCE' TAB{self.field_name} 'SEPA' 'ESPA';
"""

    def extract_results(self):
        _extract_results(self)


class CastemStressFieldResults(StressFieldResults):
    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        return f"""
NCONTRAINTES = DIME TAB3.CONTRAINTES;
TCONTRAINTES = TAB3.CONTRAINTES.(NCONTRAINTES-1);
TAB{self.field_name} = STRESSTAB TCONTRAINTES;
OPTI SORT '{self.problem.path}\\{self.field_name}';
SORT  'EXCE' TAB{self.field_name} 'SEPA' 'ESPA';
"""

    def extract_results(self):
        _extract_results(self)
