import sqlite3

from compas_fea2.problem import Problem
from compas_fea2.utilities._utils import launch_process
from compas_fea2.utilities._utils import timer


class CastemProblem(Problem):
    """Castem implementation of :class:`Problem`.\n"""

    __doc__ += Problem.__doc__

    def __init__(self, description=None, **kwargs):
        super().__init__(description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    def _build_command(self, path, name):
        return "cd {} && castem24 {}.dgibi".format(path, name)

    def analyse(
        self,
        path,
        verbose=False,
    ):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the analysis folder. A new folder with the name
            of the problem will be created at this location for all the required
            analysis files.
        save : bool
            Save structure to .cfp before the analysis.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.
        restart : bool, optional
            If `True`, save additional files for restarting the analysis later,
            by default `False`

        Returns
        -------
        None

        """
        print("\nBegin the analysis...")
        self._check_analysis_path(path)
        self.write_input_file()
        cmd = self._build_command(path=self.path, name=self.name)
        for line in launch_process(cmd_args=cmd, cwd=self.path):
            if verbose:
                print(line)

    @timer(message="Analysis and extraction completed in")
    def analyse_and_extract(
        self,
        path,
        verbose=False,
        **kwargs,
    ):
        """_summary_

        Parameters
        ----------
        path : _type_
            _description_
        exe : _type_, optional
            _description_, by default None
        cpus : int, optional
            _description_, by default 1
        output : bool, optional
            _description_, by default True
        overwrite : bool, optional
            _description_, by default True
        user_mat : _type_, optional
            _description_, by default None
        database_path : _type_, optional
            _description_, by default None
        database_name : _type_, optional
            _description_, by default None
        fields : [str], optional
            Output fields to extract from the odb file, by default None, which
            means that all available fields are extracted.

        Returns
        -------
        _type_
            _description_
        """
        self.model.assign_keys(start=self.model._key)
        self.analyse(path, verbose)
        return self.convert_results_to_sqlite()

    # ==========================================================================
    # Extract results
    # ==========================================================================
    def convert_results_to_sqlite(self, database_path=None, database_name=None, field_output=None):
        """Extract data from the Castem .inp file and store into a SQLite database.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        print("Extracting data from Castem .inp files...")
        from ..results.results_to_sql import read_results_file

        # FIXME use the ResultsDatabase class
        connection = sqlite3.connect(self.path_db)

        for step in self.steps:
            for field_output in step.field_outputs:
                read_results_file(connection, field_output)
        connection.close()
        print("Results extraction completed!")

    # =============================================================================
    #                               Job data
    # =============================================================================
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return "\n".join([step.jobdata() for step in self._steps_order])
