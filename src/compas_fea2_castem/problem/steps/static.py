import compas_fea2
from compas_fea2.problem.steps import StaticStep


class CastemStaticStep(StaticStep):
    """
    Castem implementation of the :class:`StaticStep`.

    Castem Parameters
    -------------------
    max_increments
    """

    __doc__ += StaticStep.__doc__

    def __init__(
        self,
        max_increments=1,
        initial_inc_size=1,
        min_inc_size=0.00001,
        time=1,
        nlgeom=False,
        modify=False,
        t_under_inc=0.1,
        max_under_increments=10,
        load_step=1,
        **kwargs,
    ):
        super().__init__(
            max_increments,
            initial_inc_size,
            min_inc_size,
            time,
            nlgeom,
            modify,
            **kwargs,
        )
        self.t_under_inc = t_under_inc
        self.max_under_increments = max_under_increments
        self.load_step = load_step

    # TODO : bug
    # TCAL = PROG 0. 'PAS' {self.t_under_inc} {self.time}; > self.time is False and not egal to 1....
    # TSAUV = PROG 0. 'PAS' {self.t_under_inc} {self.time};
    def jobdata(self):
        return f"""***
{self._generate_header_section()}

***
*** - LOADS
***   -------------------
*** Evolution of loading
TCAL = PROG 0. 'PAS' {self.t_under_inc} 1.;
TSAUV = PROG 0. 'PAS' {self.t_under_inc} 1.;

LISTEMP = PROG 0. 'PAS' 1. {int(1 / self.load_step)};
LISC = PROG 0. 'PAS' {self.load_step} 1.;
EVOLC = EVOL MANU 'TIME' LISTEMP 'CHARGE' LISC;

CHARTOT = VIDE 'CHARGEME';
***
*** - Displacements
***   -------------

{self._generate_displacements_section()}
***
*** - Loads
***   -------------
***
{self._generate_loads_section()}


*** - Predefined Fields
***   -----------------
***
***
*** - ANALYSIS
***   -------------------
***
TAB3 = TABLE ;
TAB3.MODELE = MODTOT ET MODJTOT;
TAB3.CARACTERISTIQUES = MATTOT ET MATJTOT;
TAB3.BLOCAGES_MECANIQUES = CLTOT ET CONTOT ET CRIGTOT;
TAB3.CHARGEMENT = CHARTOT;
TAB3.TEMPS_SAUVES = TSAUV;
TAB3.TEMPS_CALCULES = TCAL;
TAB3.MAXSOUSPAS = {self.max_under_increments};
TAB3.MAXITERATION = {self.max_increments};
TAB3.PRECISION = {self.min_inc_size};
TAB3.GRANDS_DEPLACEMENTS = {"VRAI" if self.nlgeom else "FAUX"};
TAB3.CONVERGENCE_FORCEE= FAUX;


PASAPAS TAB3;
***
*** - Output Results
***   --------------
{self._generate_output_section()}
***
"""

    def _generate_header_section(self):
        return f"""***
*** STEP {self.name} {self.problem._steps_order.index(self)}
***
"""

    def _generate_displacements_section(self):
        return "\n".join(field.jobdata() for field in self.displacements)

    # def _generate_loads_displacement_section(self):
    #     field_data = []
    #     for field in self.load_fields:
    #         if isinstance(field, compas_fea2.problem.DisplacementField):
    #             field_data.append(field.jobdata())
    #         else:
    #             field_data.append(self.combination.jobdata())

        # return "\n".join(field_data)

    def _generate_loads_section(self):
        return self.combination.jobdata()

    def _generate_fields_section(self):
        return "***"

    def _generate_output_section(self):
        data_section = ["***"]
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput.jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput.jobdata())

        return "\n".join(data_section)
