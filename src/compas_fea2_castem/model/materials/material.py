from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import UserMaterial


def jobdata(mod, mate, parameters):
    return [mod, mate, parameters]


# ==============================================================================
# linear elastic
# ==============================================================================


class CastemElasticOrthotropic(ElasticOrthotropic):
    """Castem implementation of :class:`ElasticOrthotropic`\n"""

    __doc__ += ElasticOrthotropic.__doc__
    __doc__ += """
https://www-cast3m.cea.fr/index.php?page=notices&notice=mate#MECANIQUE%20ELASTIQUE%20ORTHOTROPE115

    """

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, name=None, **kwargs):
        super(ElasticOrthotropic, self).__init__(Ex=Ex, Ey=Ey, Ez=Ez, vxy=vxy, vyz=vyz, vzx=vzx, Gxy=Gxy, Gyz=Gyz, Gzx=Gzx, density=density, name=name, **kwargs)

        self.mod = "MECANIQUE ELASTIQUE ORTHOTROPE"
        self.mate = f"'YG1' {self.Ex} 'YG2' {self.Ey} 'YG3'{self.Ez} 'NU12'{self.vxy} 'NU23'{self.vyz} 'NU13'{self.vzx} 'G12'{self.Gxy} 'G23'{self.Gyz} 'G13'{self.Gzx}"
        if self.density:
            self.mate = self.mate + " 'RHO' {}".format(self.density)
        self.complementary_line = None

    def jobdata(self):
        return jobdata(self.mod, self.mate, self.complementary_line)


class CastemElasticIsotropic(ElasticIsotropic):
    """Castem implementation of :class:`ElasticIsotropic`
    https://www-cast3m.cea.fr/index.php?page=notices&notice=mate#MECANIQUE%20ELASTIQUE%20ISOTROPE11
    \n"""

    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, E, v, density, unilateral=None, name=None, **kwargs):
        super(CastemElasticIsotropic, self).__init__(E=E, v=v, density=density, name=name, **kwargs)
        self.mod = "MECANIQUE ELASTIQUE ISOTROPE"
        self.mate = f"'YOUN' {self.E} 'NU' {self.v}"
        if self.density:
            self.mate = self.mate + " 'RHO' {}".format(self.density)
        self.complementary_line = None

    def jobdata(self):
        return jobdata(self.mod, self.mate, self.complementary_line)


# ==============================================================================
# non-linear general
# ==============================================================================


class CastemElasticPlastic(ElasticPlastic):
    """Castem implementation of :class:`ElasticPlastic`

    https://www-cast3m.cea.fr/index.php?page=notices&notice=mate#MECANIQUE%20ELASTO-PLASTIQUE16\n"""

    __doc__ += ElasticPlastic.__doc__
    __doc__ += """
    Nota CASTEM
    -----------
    The plastic model is isotrope.
    
    In castem, the strain-stress evolution must not include the elastic part and start with the values of elastic limit. 
    The curve strain-stress must begin with a (0,0) point, the second point must correspond to the elastic limit.

    """

    def __init__(self, *, E, v, density, strain_stress, name=None, **kwargs):
        super(CastemElasticPlastic, self).__init__(E=E, v=v, density=density, strain_stress=strain_stress, name=name, **kwargs)
        self.mod = "MECANIQUE ELASTIQUE ISOTROPE PLASTIQUE ISOTROPE"
        self.mate = f"'YOUN' {self.E} 'NU' {self.v} 'ECROU' STRESSSTRAIN"
        if self.density:
            self.mate = self.mate + " 'RHO' {}".format(self.density)
        self.complementary_line = [
            f"LSTRAIN = PROG. {' '.join(strain_stress[0] for strain_stress in self.strain_stress)}",
            f"LSTRESS = PROG. {' '.join(strain_stress[1] for strain_stress in self.strain_stress)}",
            "STRAINSTRESS = EVOL 'MANU' LSTRAIN LSTRESS;",
        ]

    def jobdata(self):
        return jobdata(self.mod, self.mate, self.complementary_line)


# ==============================================================================
# User-defined Materials
# ==============================================================================


class CastemUserMaterial(UserMaterial):
    """Castem implementation of :class:`UserMaterial`\n"""

    __doc__ += UserMaterial.__doc__
    __doc__ += """ User Defined Material (UMAT).

    Tho implement this type of material, a separate subroutine is required.

    Parameters
    ----------
    mod : str
        Command line added to the MODE procedure that defines the model of the material in CASTEM.
    mate : 
        specific values for material caracteristics for the MATE procedure
    parameters :
        specific other parameters, created outside of the MODE or MATE objects, needed for implementation 
    **kwars : var
        constants needed for the UMAT definition (depends on the subroutine)
    """

    def __init__(self, mod, mate, parameters, density=None, name=None, **kwargs):
        super(CastemUserMaterial, self).__init__(self, name=name, **kwargs)

        self.__name__ = "UserMaterial"
        self.__dict__.update(kwargs)
        self._name = name
        self.mod = mod
        self.mate = mate
        self.complementary_line = parameters

    def jobdata(self):
        return jobdata(self.mod, self.mate, self.complementary_line)
