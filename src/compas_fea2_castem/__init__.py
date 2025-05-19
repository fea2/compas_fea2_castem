"""
********************************************************************************
Cast3m
********************************************************************************

reference for Cast3m commands:

"""

import os
from dotenv import load_dotenv

from pydoc import ErrorDuringImport
import compas_fea2


# Models
from compas_fea2.model import Model
from compas_fea2.model import Part, RigidPart
from compas_fea2.model import Node

# Elements
from compas_fea2.model.elements import (
    LinkElement,
    BeamElement,
    ShellElement,
    TetrahedronElement,
)

# Sections
from compas_fea2.model.sections import (
    AngleSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    PipeSection,
    RectangularSection,
    ShellSection,
    SolidSection,
)

# Materials
from compas_fea2.model.materials.material import (
    ElasticIsotropic,
)
from compas_fea2.model.materials.steel import (
    Steel,
)

# Connectors
from compas_fea2.model.connectors import (
    RigidLinkConnector,
)

# Interface
from compas_fea2.model.interfaces import (
    Interface,
)

# Interaction
from compas_fea2.model.interactions import LinearContactFrictionPenalty

# Boundary Conditions
from compas_fea2.model.bcs import (
    GeneralBC,
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
from compas_fea2.problem.steps import StaticStep, ModalAnalysis

# Loads
from compas_fea2.problem.loads import ConcentratedLoad, PressureLoad, GravityLoad

# Fields
from compas_fea2.problem.fields import NodeLoadField, DisplacementField

# Displacements


# Displacements
from compas_fea2.problem.combinations import (
    LoadCombination,
)

# Outputs

# FieldResult
from compas_fea2.results.fields import (
    DisplacementFieldResults,
    ReactionFieldResults,
    StressFieldResults,
    SectionForcesFieldResults,
)

# Input File
from compas_fea2.job import (
    InputFile,
)

# =========================================================================
#                           CASTEM CLASSES
# =========================================================================

try:
    # Castem Models
    from .model import CastemModel
    from .model import CastemPart, CastemRigidPart
    from .model import CastemNode

    # Castem Elements
    from .model.elements import (
        CastemBeamElement,
        CastemShellElement,
        CastemTetrahedronElement,
        CastemLinkElement,
    )

    # # Castem Sections
    from .model.sections import (
        CastemAngleSection,
        CastemBoxSection,
        CastemCircularSection,
        CastemHexSection,
        CastemISection,
        CastemPipeSection,
        CastemRectangularSection,
        CastemShellSection,
        CastemSolidSection,
    )

    # # Castem Materials
    from .model.materials.material import (
        CastemElasticIsotropic,
    )
    from .model.materials.steel import (
        CastemSteel,
    )

    # Castem Connectors
    from .model.connectors import (
        CastemRigidLinkConnector,
    )

    # Castem Interface
    from .model.interfaces import CastemInterface

    # Castem Interaction
    from .model.interactions import CastemLinearContactFrictionPenalty

    # Castem Boundary Conditions
    from .model.bcs import (
        CastemGeneralBC,
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
    from .problem.steps import CastemStaticStep, CastemModalAnalysis

    # Castem Loads
    from .problem.loads import CastemConcentratedLoad, CastemPressureLoad, CastemGravityLoad

    # Castem Fields
    from .problem.fields import CastemNodeLoadField, CastemDisplacementField

    # Castem Combinations
    from .problem.combinations import (
        CastemLoadCombination,
    )

    # Castem field results
    from .results.fields import (
        CastemDisplacementFieldResults,
        CastemReactionFieldResults,
        CastemStressFieldResults,
        CastemSectionForcesFieldResults,
    )

    # # Castem Input File
    from .job import (
        CastemInputFile,
    )

    # build the plugin registry
    def _register_backend():
        backend = compas_fea2.BACKENDS["compas_fea2_castem"]

        backend[Model] = CastemModel
        backend[Part] = CastemPart
        backend[RigidPart] = CastemRigidPart
        backend[Node] = CastemNode

        backend[LinkElement] = CastemLinkElement
        backend[BeamElement] = CastemBeamElement
        backend[ShellElement] = CastemShellElement
        backend[TetrahedronElement] = CastemTetrahedronElement

        backend[AngleSection] = CastemAngleSection
        backend[BoxSection] = CastemBoxSection
        backend[CircularSection] = CastemCircularSection
        backend[HexSection] = CastemHexSection
        backend[ISection] = CastemISection
        backend[PipeSection] = CastemPipeSection
        backend[RectangularSection] = CastemRectangularSection
        backend[ShellSection] = CastemShellSection
        backend[SolidSection] = CastemSolidSection

        backend[ElasticIsotropic] = CastemElasticIsotropic
        backend[Steel] = CastemSteel

        backend[RigidLinkConnector] = CastemRigidLinkConnector

        backend[Interface] = CastemInterface

        backend[LinearContactFrictionPenalty] = CastemLinearContactFrictionPenalty

        backend[GeneralBC] = CastemGeneralBC
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

        backend[StaticStep] = CastemStaticStep
        backend[ModalAnalysis] = CastemModalAnalysis

        backend[ConcentratedLoad] = CastemConcentratedLoad
        backend[GravityLoad] = CastemGravityLoad
        backend[PressureLoad] = CastemPressureLoad

        backend[NodeLoadField] = CastemNodeLoadField
        backend[DisplacementField] = CastemDisplacementField

        backend[LoadCombination] = CastemLoadCombination

        backend[DisplacementFieldResults] = CastemDisplacementFieldResults
        backend[ReactionFieldResults] = CastemReactionFieldResults
        backend[StressFieldResults] = CastemStressFieldResults
        backend[SectionForcesFieldResults] = CastemSectionForcesFieldResults

        backend[InputFile] = CastemInputFile

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
