import pathlib
from collections.abc import Sequence as CollectionsSequence

Path = pathlib.Path

# This file contains the path configuration for the application.
# The paths are relative to the root of the project.
# The root path of the project
ROOT_PATH = Path(__file__).resolve().parent.parent
pathlib.Sequence = CollectionsSequence
