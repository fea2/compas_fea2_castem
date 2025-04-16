from compas_fea2.model.interactions import LinearContactFrictionPenalty


class CastemLinearContactFrictionPenalty(LinearContactFrictionPenalty):
    """Castem implementation of the :class:`LinearContactFrictionPenalty`.

    The behaviour is a Mohr Coulomb criteria with associated flow.

    Some specific output values, relative to the beaviour of the interface, can be read :


    \n"""

    __doc__ += LinearContactFrictionPenalty.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    tangentialstiffness : float
        tangentialstiffness for elactic lateral behaviour
    Cohesion : float
        initial cohesion of the behaviour for lateral behaviour
    tractionresistance : float
        tractionresistance for normal behaviour. If traction is higher than the parameter,
"""

    def __init__(self, *, stiffness, mu, normalclosingthreshold=5, tangentialstiffness=1000000000, cohesion=1000000000, tractionresistance=0, tol=0.005, **kwargs) -> None:
        super(CastemLinearContactFrictionPenalty, self).__init__(stiffness=stiffness, mu=mu, tol=tol, **kwargs)
        self._KS = tangentialstiffness
        self._KN = stiffness
        self._KCN = 2 * stiffness
        self._dCN = normalclosingthreshold
        self._mu = mu
        self._cohesion = cohesion
        self._sigmaT = tractionresistance
        self._jointmodel = "'MECANIQUE' 'ELASTIQUE' 'ISOTROPE' 'PLASTIQUE' 'COULOMB'"

    @property
    def KS(self):
        return self._KS

    @property
    def KN(self):
        return self._KN

    @property
    def KCN(self):
        return self._KCN

    @KCN.setter
    def KCN(self, value):
        self._KCN = value

    @property
    def dCN(self):
        return self._dCN

    @property
    def mu(self):
        return self._mu

    @property
    def cohesion(self):
        return self._cohesion

    @property
    def sigmaT(self):
        return self._sigmaT

    def jobdata(self):
        return f"'KN' {self._KN} 'KS' {self._KS} 'EF' {self.KCN} 'ECN' {self.dCN} 'COHE' {self.cohesion} 'FRIC' {self.mu} 'FTRC' {self.sigmaT}"
        # return f"'KN' {self._KN} 'KS' {self._KS}"
