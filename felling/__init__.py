"""
A package for consistent logging
"""
from felling.src.configure_felling import configure
from felling.src.email import send_email

__name__ = "felling"


# try:
from importlib.metadata import version as version_getter
from importlib.metadata import PackageNotFoundError as NoPackageError

try:
    __version__ = version_getter("felling")
except NoPackageError:
    __version__ = "Cannot find version"


__doc__ = """
Felling is a package which helps with logging
"""