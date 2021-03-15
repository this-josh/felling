"""
A package for consistent logging
"""
from felling.src.configure_felling import configure

__name__ = "felling"


# Felling supports multiple python versions which required different methods of getting the version
try:
    from importlib.metadata import version as version_getter
    from importlib.metadata import PackageNotFoundError as NoPackageError
except ModuleNotFoundError:
    from pkg_resources import get_distribution as version_getter
    from pkg_resources import DistributionNotFound as NoPackageError

try:
    __version__ = version_getter("felling")
except NoPackageError:
    pass