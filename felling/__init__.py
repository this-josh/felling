"""
A package for consistent logging
"""
from felling.src.configure_felling import configure

__name__ = "felling"
# combined version

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
