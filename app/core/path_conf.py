from pathlib import Path

# This file contains the path configuration for the application.
# The paths are relative to the root of the project.
# The root path of the project
ROOT_PATH = Path(__file__).resolve().parent.parent

LOG_DIR = ROOT_PATH / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
