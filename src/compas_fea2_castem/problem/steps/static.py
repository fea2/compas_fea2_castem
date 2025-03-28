from compas_fea2.problem.steps import StaticStep


class CastemStaticStep(StaticStep):
    """
    Opensees implementation of the :class:`LinearStaticStep`.

    Opensees Parameters
    -------------------
    max_increments : int, optional
        Maximum number of increments (default is 1).
    initial_inc_size : float, optional
        Initial increment size (default is 1).
    min_inc_size : float, optional
        Minimum increment size (default is 0.00001).
    constraint : str, optional
        Constraint handler (default is "Transformation").
        Possible values:
        - "Transformation": Suitable for most problems, handles constraints by transforming the system of equations.
        - "Plain": Simple constraint handler, suitable for small problems.
        - "Lagrange": Uses Lagrange multipliers, suitable for problems with multiple constraints.
        - "Penalty": Uses penalty method, suitable for problems where constraints need to be enforced strictly.
    numberer : str, optional
        Numberer (default is "RCM").
        Possible values:
        - "RCM": Reverse Cuthill-McKee, suitable for reducing bandwidth of the system matrix.
        - "Plain": Simple numberer, suitable for small problems.
    system : str, optional
        System of equations solver (default is "BandGeneral").
        Possible values:
        - "BandGeneral": General band solver, suitable for most problems.
        - "ProfileSPD": Profile solver for symmetric positive definite matrices, suitable for specific problems.
        - "SuperLU": Direct solver using SuperLU, suitable for large sparse systems.
        - "UmfPack": Direct solver using UMFPACK, suitable for large sparse systems.
    test : str, optional
        Convergence test (default is "NormDispIncr 1.0e-6, 10").
        Possible values:
        - "NormDispIncr": Checks norm of displacement increments, suitable for most problems.
        - "NormUnbalance": Checks norm of unbalanced forces, suitable for problems with force convergence criteria.
        - "NormDispAndUnbalance": Checks both displacement increments and unbalanced forces, suitable for strict convergence criteria.
    integrator : str, optional
        Integrator (default is "LoadControl").
        Possible values:
        - "LoadControl": Suitable for load-controlled problems.
        - "DisplacementControl": Suitable for displacement-controlled problems.
        - "ArcLength": Suitable for problems with snap-through or snap-back behavior.
    analysis : str, optional
        Analysis type (default is "Static").
        Possible values:
        - "Static": Suitable for static analysis.
        - "Transient": Suitable for transient analysis.
    time : float, optional
        Total time of the step (default is 1).
    nlgeom : bool, optional
        Nonlinear geometry flag (default is False).
    modify : bool, optional
        Modify flag (default is True).
    algorithm : str, optional
        Solution algorithm (default is "Newton").
        Possible values:
        - "Newton": Standard Newton-Raphson method, suitable for most problems.
        - "ModifiedNewton": Modified Newton-Raphson method, suitable for problems with convergence issues.
        - "BFGS": Broyden-Fletcher-Goldfarb-Shanno method, suitable for large-scale optimization problems.
        - "KrylovNewton": Krylov-Newton method, suitable for large sparse systems.
        - "SecantNewton": Secant-Newton method, suitable for problems with non-smooth behavior.
        - "PeriodicNewton": Periodic Newton-Raphson method, suitable for periodic problems.
    name : str, optional
        Name of the step.
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

    # TODO : bug
    # TCAL = PROG 0. 'PAS' {self.t_under_inc} {self.time}; > self.time is False and not egal to 1....
    # TSAUV = PROG 0. 'PAS' {self.t_under_inc} {self.time};
    def jobdata(self):
        return f"""***
{self._generate_header_section()}
*** - Displacements
***   -------------
{self._generate_displacements_section()}
***
*** - Loads
***   -------------
*** Evolution definition
TCAL = PROG 0. 'PAS' {self.t_under_inc} 1.;
TSAUV = PROG 0. 'PAS' {self.t_under_inc} 1.;

LISTEMP = PROG 0. 1.;
LISC = PROG 0. 1.;
EVOLC = EVOL MANU 'TIME' LISTEMP 'CHARGE' LISC;

CHARTOT = VIDE 'CHARGEME';
{self._generate_loads_section()}
***
*** - Predefined Fields
***   -----------------
{self._generate_fields_section()}
***
***
*** - ANALYSIS
***   -------------------
***
TAB3 = TABLE ;
TAB3.MODELE = MODTOT;
TAB3.CARACTERISTIQUES = MATTOT;
TAB3.BLOCAGES_MECANIQUES = CLTOT ET CONTOT;
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
        return "***"

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
