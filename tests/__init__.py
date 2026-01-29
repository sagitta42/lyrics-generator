import os
from pathlib import Path

PATH_CURRENT = os.path.dirname(__file__)

# FIXME: recycle examples or make own fixtures to not rely on examples?
EXAMPLES_DIR = Path(PATH_CURRENT) / ".." / "examples"
STANDARD_TEST = EXAMPLES_DIR / "into_glory_ride.txt"
SETTINGS_DIR = Path(PATH_CURRENT) / "settings"
