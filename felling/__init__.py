"""
A package for consistent logging
"""
from felling.src.configure_felling import configure

__name__ = "felling"


print("In felling __init__")

# Felling supports multiple python versions which required different methods of getting the version
try:
    from importlib.metadata import version as version_getter
    from importlib.metadata import PackageNotFoundError as NoPackageError
    print("importlib")
except ModuleNotFoundError:
    from pkg_resources import get_distribution as version_getter
    from pkg_resources import DistributionNotFound as NoPackageError
    print("pkg_resources")
except:
    raise ModuleNotFoundError("Neither importlib nor pkg_resources are installed")

try:
    __version__ = version_getter("felling")
except NoPackageError:
    pass