import logging
from typing import Any, Dict, Optional, Sequence, Union, List
from types import ModuleType
from numbers import Integral
from pathlib import Path
from logging.config import dictConfig
import subprocess
import subprocess
import getpass
import json
import pkg_resources
import inspect
from os.path import basename

logger = logging.getLogger("Initial logs")


def _update_filenames(
    config: Dict[str, Any],
    file_name: str,
    log_path: Path,
) -> Dict[str, Any]:
    """Create a new file name for each time the code is run

    Parameters
    ----------
    config : Dict[str, str]
        The logging config dictionary from logger.json
    file_name : str
        The file name that is to be used
    log_path : Path
        The path to save the logs to

    Returns
    -------
    Dict[str, str]
        The amended logging config dictionary
    """
    from datetime import datetime as dt

    file_name = dt.now().strftime("%y%m%d-%H%M_") + file_name
    log_path = log_path / (file_name + ".log")

    config["handlers"]["file_handler"]["filename"] = log_path

    return config


def _get_git_commit_hash() -> str:
    """Get the most recent git commit hash"""
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("UTF-8")
            .strip()
        )
    except subprocess.CalledProcessError as e:
        logger.error(str(e))
        return "Failed to read git commit hash."


def _get_git_branch_and_remote():

    logger = logging.getLogger("Initial logs")

    try:
        return subprocess.check_output(["git", "remote", "show", "origin"]).decode('UTF-8')
    except subprocess.CalledProcessError:
        logger.error("Failed to get remote git info. Does your repo have a remote?")


def _initial_logs():
    """write some initial logs"""
    # write the user name

    logger.info(f"Username: {getpass.getuser()}")
    logger.info(f"Most recent git commit hash: {_get_git_commit_hash()}")
    logger.info(f"Git remote and branch info: {_get_git_branch_and_remote()}")


def _log_versions(packages_to_log):
    """Use this to log which version of dependent packages are being used"""
    if packages_to_log is None:
        return
    for pack in packages_to_log:
        try:
            logger.info(
                f"Package {pack.__name__} has version number {pack.__version__}"
            )
        except ModuleNotFoundError as e:
            logger.info(f"Failed to log {pack} version, {e}")


def _specific_modules(config, modules: Optional[Union[str, Sequence[str]]]):
    if modules is not None:
        modules = [modules] if isinstance(modules, str) else modules
        for error_only_module in modules:
            logger.info(f"{error_only_module} will only have errors logged")
            config["loggers"][error_only_module] = config["loggers"]["Error only"]


def configure(
    log_path: Path,
    file_name: Optional[str] = None,
    file_log_level: Optional[str] = "DEBUG",
    std_out_log_level: Optional[str] = "INFO",
    error_only_modules: Optional[Union[str, Sequence[str]]] = None,
    modules_to_debug: Optional[str] = None,
    package_versions_to_log: Optional[ModuleType] = None,
):
    """Generate a logger

    Produces a consistent style of logger, editing the json file allows it to easily be modified

    Parameters
    ----------
    log_path : Path
        The path to save the logs to, must be a path otherwise could get relative location issues.
    file_name : Optional[str], default is None
        The file name that is being run, if blank it will be inferred
    debug : Optional[bool], default is False
        Whether to include debug messages
    """
    # Check if logging is enabled
    if not logging.root.isEnabledFor(50):
        print(
            "Logging has been disabled at root, `logging.root.isEnabledFor(50)` is False. Felling will not run."
        )
        return

    if not isinstance(log_path, Path):
        raise TypeError(f"log_path must be a pathlib Path, not {type(log_path)}")

    if not log_path.is_dir():
        # Ironically print as logs are not yet set up
        # TODO: set up simple config?
        logger.warning(f"Log path does not exist, will create {log_path.absolute()}")
        log_path.mkdir()

    # read in logger config
    with open(
        pkg_resources.resource_filename("felling", "logger.json"), "rt"
    ) as json_file:
        config = json.load(json_file)

    _specific_modules(config, error_only_modules)
    _specific_modules(config, modules_to_debug)

    config["handlers"]["file_handler"]["level"] = file_log_level
    config["handlers"]["console"]["level"] = std_out_log_level

    # Get name of file which called this

    caller = basename(inspect.stack()[1][1]).replace(".py", "")
    file_name = caller if file_name is None else file_name

    # update log file names
    config = _update_filenames(config, file_name, log_path)

    # configure logger
    dictConfig(config)
    _initial_logs()
    _log_versions(package_versions_to_log)
