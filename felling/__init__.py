"""
A package for consistent logging
"""
from felling.src.configure_felling import configure

__name__ = "felling"
xyversion = "0.0.2"
release = ""
# combined version
__version__ = f"{xyversion}{release}"

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
