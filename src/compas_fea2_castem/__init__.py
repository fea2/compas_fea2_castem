"""
********************************************************************************
Opensees
********************************************************************************

reference for OpenSees commands:
https://opensees.github.io/OpenSeesDocumentation/user/userManual.html


.. currentmodule:: compas_fea2_opensees


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
from dotenv import load_dotenv

from pydoc import ErrorDuringImport
import compas_fea2


# Models
from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import Node

# Elements
from compas_fea2.model.elements import (
    # MassElement,
    # LinkElement,
    BeamElement,
    # TrussElement,
    # MembraneElement,
    ShellElement,
    _Element3D,
    TetrahedronElement,
)

# Sections
from compas_fea2.model.sections import (
    # AngleSection,
    # BeamSection,
    # GenericBeamSection,
    # BoxSection,
    # CircularSection,
    # HexSection,
    # ISection,
    # MassSection,
    # PipeSection,
    RectangularSection,
    # SpringSection,
    # StrutSection,
    # TieSection,
    # TrapezoidalSection,
    # TrussSection,
    # MembraneSection,
    ShellSection,
    SolidSection,
)

# Materials
from compas_fea2.model.materials.material import (
    ElasticIsotropic,
    # ElasticOrthotropic,
    # ElasticPlastic,
    # Stiff,
    # UserMaterial,
)

# from compas_fea2.model.materials.concrete import (
#     Concrete,
#     ConcreteDamagedPlasticity,
#     ConcreteSmearedCrack,
# )
# from compas_fea2.model.materials.steel import (
#     Steel,
# )

# Groups
# from compas_fea2.model.groups import (
#     NodesGroup,
#     ElementsGroup,
#     FacesGroup,
# )

# Constraints
# from compas_fea2.model.constraints import (
#     TieConstraint,
# )

# Connectors
from compas_fea2.model.connectors import (
    RigidLinkConnector,
    #     SpringConnector,
    #     ZeroLengthSpringConnector,
    #     ZeroLengthContactConnector,
)

# Releases
# from compas_fea2.model.releases import (
#     BeamEndPinRelease,
# )

# Boundary Conditions
from compas_fea2.model.bcs import (
    FixedBC,
    FixedBCX,
    FixedBCY,
    FixedBCZ,
    ClampBCXX,
    ClampBCYY,
    ClampBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Problem
from compas_fea2.problem import Problem

# Steps
from compas_fea2.problem.steps import (
    # ModalAnalysis,
    # ComplexEigenValue,
    StaticStep,
    # LinearStaticPerturbation,
    # BucklingAnalysis,
    # DynamicStep,
    # QuasiStaticStep,
    # DirectCyclicStep,
)

# Loads
from compas_fea2.problem.loads import (
    ConcentratedLoad,
    # PressureLoad,
    # TributaryLoad,
    # PrestressLoad,
    # GravityLoad,
    # HarmonicPointLoad,
    # HarmonicPressureLoad,
)

# Displacements
# from compas_fea2.problem.displacements import (
#     GeneralDisplacement,
# )

# Displacements
from compas_fea2.problem.combinations import (
    LoadCombination,
)

# Outputs

# FieldResult
from compas_fea2.results.fields import (
    DisplacementFieldResults,
    # AccelerationFieldOutput,
    # VelocityFieldOutput,
    ReactionFieldResults,
    # Stress2DFieldOutput,
    SectionForcesFieldResults,
    # HistoryOutput,
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)

# =========================================================================
#                           CASTEM CLASSES
# =========================================================================

try:
    # Castem Models
    from .model import CastemModel
    from .model import CastemPart
    from .model import CastemNode

    # Castem Elements
    from .model.elements import (
        #     OpenseesMassElement,
        #     OpenseesLinkElement,
        CastemBeamElement,
        #     OpenseesTrussElement,
        #     OpenseesMembraneElement,
        CastemShellElement,
        _CastemElement3D,
        CastemTetrahedronElement,
    )

    # # Castem Sections
    from .model.sections import (
        #     OpenseesAngleSection,
        #     OpenseesBeamSection,
        #     OpenseesGenericBeamSection,
        #     OpenseesBoxSection,
        #     OpenseesCircularSection,
        #     OpenseesHexSection,
        #     OpenseesISection,
        #     OpenseesMassSection,
        #     OpenseesPipeSection,
        CastemRectangularSection,
        #     OpenseesSpringSection,
        #     OpenseesStrutSection,
        #     OpenseesTieSection,
        #     OpenseesTrapezoidalSection,
        #     OpenseesTrussSection,
        #     OpenseesMembraneSection,
        CastemShellSection,
        CastemSolidSection,
    )

    # # Opensees Materials
    from .model.materials.material import (
        CastemElasticIsotropic,
        #     OpenseesElasticOrthotropic,
        #     OpenseesElasticPlastic,
        #     OpenseesStiff,
        #     OpenseesUserMaterial,
    )

    # from .model.materials.concrete import (
    #     OpenseesConcrete,
    #     OpenseesConcreteDamagedPlasticity,
    #     OpenseesConcreteSmearedCrack,
    # )
    # from .model.materials.steel import (
    #     OpenseesSteel,
    # )

    # # Opensees Groups
    # from .model.groups import (
    #     OpenseesNodesGroup,
    #     OpenseesElementsGroup,
    #     OpenseesFacesGroup,
    # )

    # # Opensees Constraints
    # from .model.constraints import (
    #     OpenseesTieConstraint,
    # )

    # Opensees Connectors
    from .model.connectors import (
        CastemRigidLinkConnector,
        #     OpenseesSpringConnector,
        #     OpenseesZeroLengthSpringConnector,
        #     OpenseesZeroLengthContactConnector,
    )

    # # Opensees release
    # from .model.releases import (
    #     OpenseesBeamEndPinRelease,
    # )

    # Castem Boundary Conditions
    from .model.bcs import (
        CastemFixedBC,
        CastemFixedBCX,
        CastemFixedBCY,
        CastemFixedBCZ,
        CastemClampBCXX,
        CastemClampBCYY,
        CastemClampBCZZ,
        CastemPinnedBC,
        CastemRollerBCX,
        CastemRollerBCXY,
        CastemRollerBCXZ,
        CastemRollerBCY,
        CastemRollerBCYZ,
        CastemRollerBCZ,
    )

    # Castem Problem
    from .problem import CastemProblem

    # Castem Steps
    from .problem.steps import (
        #     OpenseesModalAnalysis,
        #     OpenseesComplexEigenValue,
        CastemStaticStep,
        #     OpenseesLinearStaticPerturbation,
        #     OpenseesBucklingAnalysis,
        #     OpenseesDynamicStep,
        #     OpenseesQuasiStaticStep,
        #     OpenseesDirectCyclicStep,
    )

    # Castem Loads
    from .problem.loads import (
        CastemConcentratedLoad,
        #     OpenseesPressureLoad,
        #     OpenseesTributaryLoad,
        #     OpenseesPrestressLoad,
        #     OpenseesGravityLoad,
        #     OpenseesHarmonicPointLoad,
        #     OpenseesHarmonicPressureLoad,
    )

    # # Opensees Displacements
    # from .problem.displacements import (
    #     OpenseesGeneralDisplacement,
    # )

    # Castem Displacements
    from .problem.combinations import (
        CastemLoadCombination,
    )

    # Castem field results
    from .results.fields import (
        CastemDisplacementFieldResults,
        #     OpenseesAccelerationFieldOutput,
        #     OpenseesVelocityFieldOutput,
        CastemReactionFieldResults,
        #     OpenseesStress2DFieldOutput,
        CastemSectionForcesFieldResults,
        #     OpenseesHistoryOutput,
    )

    # # Opensees Input File
    from .job import (
        CastemInputFile,
        CastemParametersFile,
    )

    # build the plugin registry
    def _register_backend():
        backend = compas_fea2.BACKENDS["compas_fea2_castem"]

        backend[Model] = CastemModel
        backend[Part] = CastemPart
        backend[Node] = CastemNode

        # backend[MassElement] = OpenseesMassElement
        # backend[LinkElement] = OpenseesLinkElement
        backend[BeamElement] = CastemBeamElement
        # backend[TrussElement] = OpenseesTrussElement
        # backend[MembraneElement] = OpenseesMembraneElement
        backend[ShellElement] = CastemShellElement
        backend[_Element3D] = _CastemElement3D
        backend[TetrahedronElement] = CastemTetrahedronElement

        # backend[AngleSection] = OpenseesAngleSection
        # backend[BeamSection] = OpenseesBeamSection
        # backend[GenericBeamSection] = OpenseesGenericBeamSection
        # backend[BoxSection] = OpenseesBoxSection
        # backend[CircularSection] = OpenseesCircularSection
        # backend[HexSection] = OpenseesHexSection
        # backend[ISection] = OpenseesISection
        # backend[MassSection] = OpenseesMassSection
        # backend[MembraneSection] = OpenseesMembraneSection
        # backend[PipeSection] = OpenseesPipeSection
        backend[RectangularSection] = CastemRectangularSection
        backend[ShellSection] = CastemShellSection
        backend[SolidSection] = CastemSolidSection
        # backend[SpringSection] = OpenseesSpringSection
        # backend[StrutSection] = OpenseesStrutSection
        # backend[TieSection] = OpenseesTieSection
        # backend[TrapezoidalSection] = OpenseesTrapezoidalSection
        # backend[TrussSection] = OpenseesTrussSection

        backend[ElasticIsotropic] = CastemElasticIsotropic
        # backend[ElasticOrthotropic] = OpenseesElasticOrthotropic
        # backend[ElasticPlastic] = OpenseesElasticPlastic
        # backend[Stiff] = OpenseesStiff
        # backend[UserMaterial] = OpenseesUserMaterial
        # backend[Concrete] = OpenseesConcrete
        # backend[ConcreteDamagedPlasticity] = OpenseesConcreteDamagedPlasticity
        # backend[ConcreteSmearedCrack] = OpenseesConcreteSmearedCrack
        # backend[Steel] = OpenseesSteel

        # backend[NodesGroup] = OpenseesNodesGroup
        # backend[ElementsGroup] = OpenseesElementsGroup
        # backend[FacesGroup] = OpenseesFacesGroup

        # backend[TieConstraint] = OpenseesTieConstraint

        backend[RigidLinkConnector] = CastemRigidLinkConnector
        # backend[SpringConnector] = OpenseesSpringConnector
        # backend[ZeroLengthSpringConnector] = OpenseesZeroLengthSpringConnector
        # backend[ZeroLengthContactConnector] = OpenseesZeroLengthContactConnector

        # backend[BeamEndPinRelease] = OpenseesBeamEndPinRelease

        backend[FixedBC] = CastemFixedBC
        backend[FixedBCX] = CastemFixedBCX
        backend[FixedBCY] = CastemFixedBCY
        backend[FixedBCZ] = CastemFixedBCZ
        backend[ClampBCXX] = CastemClampBCXX
        backend[ClampBCYY] = CastemClampBCYY
        backend[ClampBCZZ] = CastemClampBCZZ
        backend[PinnedBC] = CastemPinnedBC
        backend[RollerBCX] = CastemRollerBCX
        backend[RollerBCXY] = CastemRollerBCXY
        backend[RollerBCXZ] = CastemRollerBCXZ
        backend[RollerBCY] = CastemRollerBCY
        backend[RollerBCYZ] = CastemRollerBCYZ
        backend[RollerBCZ] = CastemRollerBCZ

        backend[Problem] = CastemProblem

        # backend[ModalAnalysis] = OpenseesModalAnalysis
        # backend[ComplexEigenValue, StaticStep] = OpenseesComplexEigenValue
        backend[StaticStep] = CastemStaticStep
        # backend[LinearStaticPerturbation] = OpenseesLinearStaticPerturbation
        # backend[BucklingAnalysis] = OpenseesBucklingAnalysis
        # backend[DynamicStep] = OpenseesDynamicStep
        # backend[QuasiStaticStep] = OpenseesQuasiStaticStep
        # backend[DirectCyclicStep] = OpenseesDirectCyclicStep

        # backend[GravityLoad] = OpenseesGravityLoad
        backend[ConcentratedLoad] = CastemConcentratedLoad
        # backend[PressureLoad] = OpenseesPressureLoad
        # backend[TributaryLoad] = OpenseesTributaryLoad
        # backend[PrestressLoad] = OpenseesPrestressLoad
        # backend[HarmonicPointLoad] = OpenseesHarmonicPointLoad
        # backend[HarmonicPressureLoad] = OpenseesHarmonicPressureLoad

        # backend[GeneralDisplacement] = OpenseesGeneralDisplacement

        backend[LoadCombination] = CastemLoadCombination

        # backend[HistoryOutput] = OpenseesHistoryOutput

        backend[DisplacementFieldResults] = CastemDisplacementFieldResults
        # backend[AccelerationFieldOutput] = OpenseesAccelerationFieldOutput
        # backend[VelocityFieldOutput] = OpenseesVelocityFieldOutput
        backend[ReactionFieldResults] = CastemReactionFieldResults
        # backend[Stress2DFieldOutput] = OpenseesStress2DFieldOutput
        backend[SectionForcesFieldResults] = CastemSectionForcesFieldResults

        backend[InputFile] = CastemInputFile
        backend[ParametersFile] = CastemParametersFile

        print("Castem implementations registered...")

except ImportError:
    raise ErrorDuringImport()


def init_fea2_castem(exe):
    """Create a default environment file if it doesn't exist and loads its variables.

    Parameters
    ----------
    verbose : bool, optional
        Be verbose when printing output, by default False
    point_overlap : bool, optional
        Allow two nodes to be at the same location, by default True
    global_tolerance : int, optional
        Tolerance for the model, by default 1
    precision : str, optional
        Values approximation, by default '3f'

    """

    env_path = os.path.abspath(os.path.join(HERE, ".env"))
    with open(env_path, "x") as f:
        f.write(
            "\n".join(
                [
                    "EXE={}".format(exe),
                ]
            )
        )
    load_dotenv(env_path)


__author__ = ["Ines Champagne"]
__copyright__ = "Ines Champagne"
__license__ = "MIT License"
__email__ = "ines.champagne@gmail.com"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
