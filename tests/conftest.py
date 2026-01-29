import sys
import os

from . import PATH_CURRENT

# make src modules accessible in all test_* files without having to install the package
path_to_src = os.path.join(PATH_CURRENT, "..", "src")
path_to_src_absolute = os.path.abspath(path_to_src)

sys.path.insert(0, path_to_src_absolute)
