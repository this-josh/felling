import logging
from typing import Any, Dict, Optional, Sequence, Union, List
from types import ModuleType
from pathlib import Path
from datetime import datetime as dt
from logging.config import dictConfig
import subprocess
import getpass
import json
import pkg_resources
import inspect

logger = logging.getLogger("Initial logs")


def _update_filenames(
    config: Dict[str, Any],
    log_file_name: str,
    log_path: Path,
) -> Dict[str, Any]:
    """Create a new file name for each time the code is run

    Parameters
    ----------
    config : Dict[str, str]
        The logging config dictionary from logger.json
    log_file_name : str
        The file name that is to be used
    log_path : Path
        The path to save the logs to

    Returns
    -------
    Dict[str, str]
        The amended logging config dictionary
    """

    log_file_name = dt.now().strftime("%y%m%d-%H%M_") + log_file_name
    log_path = log_path / (log_file_name + ".log")

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
    """Get information about the git branch and remote"""
    try:
        return subprocess.check_output(["git", "remote", "show", "origin"]).decode(
            "UTF-8"
        )
    except subprocess.CalledProcessError:
        logger.error("Failed to get remote git info. Does your repo have a remote?")


def _initial_logs():
    """write some initial logs"""
    logger.info(f"Username: {getpass.getuser()}")
    logger.info(f"Most recent git commit hash: {_get_git_commit_hash()}")
    logger.info(f"Git remote and branch info: {_get_git_branch_and_remote()}")


def _log_versions(packages_to_log: Optional[List[ModuleType]]):
    """Use this to log which version of dependent packages are being used"""
    if packages_to_log is None:
        return
    if isinstance(packages_to_log, ModuleType):
        packages_to_log = [packages_to_log]
    for pack in packages_to_log:
        try:
            logger.info(
                f"Package {pack.__name__} has version number {pack.__version__}"
            )
        except ModuleNotFoundError as e:
            logger.info(f"Failed to log {pack} version, {e}")
        except Exception as e:
            logger.exception(e.args)
            logger.info(f"{pack} version will not be logged.")


def _specific_modules(
    config: Dict[str, Any],
    modules: Optional[Union[str, Sequence[str]]],
    debug_or_error: str,
) -> Dict[str, Any]:
    """
    Give specific modules their own handlers

    Parameters
    ----------
    config : Dict[str, Any]
        The config data
    modules : Optional[Union[str, Sequence[str]]]
        Modules to give handlers
    debug_or_error : str
        Must be either "ERROR" or "DEBUG", whether to give handlers for errors or debug

    Returns
    -------
    Dict[str, Any]
        The modified config data
    """

    if modules is not None:
        modules = [modules] if isinstance(modules, str) else modules
        for module in modules:
            logger.info(f"{module} will only have {debug_or_error} logged")
            config["loggers"][module] = config["loggers"][f"{debug_or_error} only"]
    return config


def configure(
    log_path: Union[Path, str, None] = None,
    log_file_name: Optional[str] = None,
    file_log_level: Optional[str] = "DEBUG",
    std_out_log_level: Optional[str] = "INFO",
    error_only_modules: Optional[Union[str, Sequence[str]]] = None,
    modules_to_debug: Optional[str] = None,
    package_versions_to_log: Optional[Union[ModuleType, List[ModuleType]]] = None,
):
    """
    Configure logging for this run time

    Parameters
    ----------
    log_path : Union[Path, str, None], optional
        The path to save logs to, by default None
    log_file_name : Optional[str], optional
        The log file name, by default None
    file_log_level : Optional[str], optional
        The minimum log level to write to file, by default "DEBUG"
    std_out_log_level : Optional[str], optional
        The minimum log level to write to std out, by default "INFO"
    error_only_modules : Optional[Union[str, Sequence[str]]], optional
        Modules to only log errors, by default None
    modules_to_debug : Optional[str], optional
        Modules to log debug logs, by default None
    package_versions_to_log : Optional[ModuleType], optional
        Packages to log versions for, by default None
    """
    # Check if logging is enabled
    if not logging.root.isEnabledFor(50):
        print(
            "Logging has been disabled at root, `logging.root.isEnabledFor(50)` is False. Felling will not run."
        )
        return

    caller_info = Path(inspect.stack()[1].filename)

    if isinstance(log_path, str):
        log_path = Path(log_path)
    elif log_path is None:
        print(
            f"Log path is {log_path}, a folder 'logs' will be created in the same dir as __main__"
        )
        log_path = caller_info.parent / "logs"

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

    config = _specific_modules(config, error_only_modules, "ERROR")
    config = _specific_modules(config, modules_to_debug, "DEBUG")

    config["handlers"]["file_handler"]["level"] = file_log_level
    config["handlers"]["console"]["level"] = std_out_log_level

    # update log file names
    log_file_name = caller_info.stem if log_file_name is None else log_file_name
    config = _update_filenames(config, log_file_name, log_path)

    # configure logger
    dictConfig(config)
    _initial_logs()
    _log_versions(package_versions_to_log)
