from app.core.constants import ROOT_PATH

LOG_DIR = ROOT_PATH / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = ROOT_PATH / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
