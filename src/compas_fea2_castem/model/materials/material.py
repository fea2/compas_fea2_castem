from compas_fea2.model import ElasticIsotropic


# ==============================================================================
# linear elastic
# ==============================================================================
class CastemElasticIsotropic(ElasticIsotropic):
    """Castem implementation of :class:`ElasticIsotropic`\n"""

    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, E, v, density, **kwargs):
        super(CastemElasticIsotropic, self).__init__(E=E, v=v, density=density, **kwargs)

    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        data = ["MECANIQUE ELASTIQUE ISOTROPE", f"'YOUN' {self.E} 'NU' {self.v}" + f" 'RHO' {self.density}" if self.density else ""]
        return data
