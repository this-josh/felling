import logging
from logging import exception, log
from typing import Dict, Optional, Union
from pathlib import Path

logger = logging.getLogger("Initial logs")


def _update_filenames(
    config: Dict[str, str], file_name: str, log_path: Path
) -> Dict[str, str]:
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
    debug_log_path = log_path / (file_name + "_debug.log")
    info_log_path = log_path / (file_name + "_info.log")
    warning_log_path = log_path / (file_name + "_warning.log")

    config["handlers"]["debug_file_handler"]["filename"] = debug_log_path
    config["handlers"]["info_file_handler"]["filename"] = info_log_path
    config["handlers"]["warning_file_handler"]["filename"] = warning_log_path

    return config


def _get_git_commit_hash():
    import subprocess

    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"])
    except subprocess.CalledProcessError as e:
        logger.error(str(e))
        return "Failed to read git commit hash."


def _get_git_branch_and_remote():
    import subprocess

    logger = logging.getLogger("Initial logs")

    # TODO: This output should be formatted better
    try:
        return subprocess.check_output(["git", "remote", "show", "origin"])
    except subprocess.CalledProcessError:
        logger.exception("Failed to get remote git info.")


def _initial_logs():
    """write some initial logs"""
    # write the user name
    import getpass

    logger.info(f"Username: {getpass.getuser()}")
    logger.info(f"Most recent git commit hash: {_get_git_commit_hash()}")
    logger.info(f"Git remote and branch info: {_get_git_branch_and_remote()}")


def _log_versions():
    """Use this to log which version of dependent packages are being used"""
    logger.debug("Not currently logging versions")


def configure_logger(
    log_path: Path,
    file_name: Optional[str] = None,
    debug=True,
    specific_module: Optional[str] = None,
):
    """Generate a logger

    Produces a consistent style of logger, editing the json file allows it to easily be modified

    Parameters
    ----------
    log_path : Path
        The path to save the logs to, must be a path otherwise could get relative location issues.
    file_name : Optional[str], default is None
        The file name that is being run, if blank it will be inferred
    debug : Optional[bool], default is True
        Whether to include debug messages
    """
    import logging.config
    import json
    import pkg_resources
    import inspect

    # Check if logging is enabled
    if logging.root.manager.disable >= 50:
        return
    # read in logger config
    with open(
        pkg_resources.resource_filename("easy_logger", "logger.json"), "rt"
    ) as json_file:
        config = json.load(json_file)

    if specific_module is not None:
        logger.info(f"{specific_module} will get its own handler")
        config["loggers"][specific_module] = config["loggers"]["specific module"]
    if debug is False:
        config["root"]["level"] = "INFO"
    # Get name of file which called this
    from os.path import basename

    caller = basename(inspect.stack()[1][1]).replace(".py", "")
    if file_name == None:
        file_name = caller

    # update log file names
    config = _update_filenames(config, file_name, log_path)

    # configure logger
    logging.config.dictConfig(config)
    _initial_logs()
    _log_versions()
