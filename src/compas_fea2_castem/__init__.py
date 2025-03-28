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
from compas_fea2.model import Part
from compas_fea2.model import Node

# Elements
from compas_fea2.model.elements import (
    LinkElement,
    BeamElement,
    ShellElement,
    _Element3D,
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

# Connectors
from compas_fea2.model.connectors import (
    RigidLinkConnector,
)


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
from compas_fea2.problem.steps import (
    StaticStep,
)

# Loads
from compas_fea2.problem.loads import (
    ConcentratedLoad,
)

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
    from .model import CastemPart
    from .model import CastemNode

    # Castem Elements
    from .model.elements import (
        CastemBeamElement,
        CastemShellElement,
        _CastemElement3D,
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

    # # Opensees Materials
    from .model.materials.material import (
        CastemElasticIsotropic,
    )

    # Opensees Connectors
    from .model.connectors import (
        CastemRigidLinkConnector,
    )

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
    from .problem.steps import (
        CastemStaticStep,
    )

    # Castem Loads
    from .problem.loads import (
        CastemConcentratedLoad,
    )

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

    # # Opensees Input File
    from .job import (
        CastemInputFile,
    )

    # build the plugin registry
    def _register_backend():
        backend = compas_fea2.BACKENDS["compas_fea2_castem"]

        backend[Model] = CastemModel
        backend[Part] = CastemPart
        backend[Node] = CastemNode

        backend[LinkElement] = CastemLinkElement
        backend[BeamElement] = CastemBeamElement
        backend[ShellElement] = CastemShellElement
        backend[_Element3D] = _CastemElement3D
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

        backend[RigidLinkConnector] = CastemRigidLinkConnector

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

        backend[ConcentratedLoad] = CastemConcentratedLoad

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
