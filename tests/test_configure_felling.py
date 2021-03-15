import os
import re
from pathlib import Path
import shutil
import pytest
import logging

str_log_path = "./tests/logs"


def test_configure_default_path():
    """Quick sanity check test"""
    from felling.src.configure_felling import configure

    shutil.rmtree(str_log_path, ignore_errors=True)

    configure()

    assert len(os.listdir(str_log_path)) == 1
    shutil.rmtree(str_log_path)


def test_configure_str_path():
    """Quick sanity check test"""
    from felling.src.configure_felling import configure

    log_path = "./tests/logs_str"
    shutil.rmtree(log_path, ignore_errors=True)

    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_pathlib_path():
    """Quick sanity check test"""
    from felling.src.configure_felling import configure

    log_path = Path("./tests/logs_path")
    shutil.rmtree(log_path, ignore_errors=True)

    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_file_name():
    """Check custom file names are working"""
    from felling.src.configure_felling import configure

    log_path = Path(str_log_path)
    shutil.rmtree(log_path, ignore_errors=True)
    file_name = "test_log"
    configure(log_path, log_file_name=file_name)

    assert len(os.listdir(log_path)) == 1

    assert (
        re.match(r"^[0-9]{8}-[0-9]{4}_" + file_name + ".log", os.listdir(log_path)[0])
        is not None
    )

    shutil.rmtree(log_path)


def test_update_filenames():
    from felling.src.configure_felling import _update_filenames

    config = {"handlers": {"file_handler": {"filename": "NOT A FILENAME"}}}
    log_path = Path("./logs")
    log_file_name = "test_file_name"
    config = _update_filenames(config, log_file_name, log_path)
    assert (
        re.match(
            r"^[0-9]{8}-[0-9]{4}_" + log_file_name + ".log",
            config["handlers"]["file_handler"]["filename"].name,
        )
        is not None
    )


def test_initial_logs():
    from felling.src.configure_felling import _initial_logs

    _initial_logs()


def test_log_versions_no_package():
    from felling.src.configure_felling import _log_versions

    assert _log_versions(None) is None


def test_log_versions_one_package():
    from felling.src.configure_felling import _log_versions

    assert _log_versions(re) is None


def test_log_versions_multiple_package():
    from felling.src.configure_felling import _log_versions

    assert _log_versions([logging, re]) is None


def test_log_versions_invalid_package():
    from felling.src.configure_felling import _log_versions

    with pytest.raises(AttributeError):
        assert _log_versions(os) is None


def test_log_versions_other_error():
    from felling.src.configure_felling import _log_versions

    with pytest.raises(TypeError, match="'int' object is not iterable"):
        assert _log_versions(3) is None


def test_specific_modules_one_module_error_only():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"ERROR only": "ERROR only handler"}}
    config = _specific_modules(config, re, "ERROR")
    assert config["loggers"]["re"] == "ERROR only handler"


def test_specific_modules_multiple_module_error_only():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"ERROR only": "ERROR only handler"}}
    config = _specific_modules(config, [re, os], "ERROR")
    assert config["loggers"]["re"] == "ERROR only handler"
    assert config["loggers"]["os"] == "ERROR only handler"


def test_specific_modules_one_module_debug_only():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    config = _specific_modules(config, re, "DEBUG")
    assert config["loggers"]["re"] == "DEBUG only handler"


def test_specific_modules_multiple_module_debug_only():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    config = _specific_modules(config, [re, os], "DEBUG")
    assert config["loggers"]["re"] == "DEBUG only handler"
    assert config["loggers"]["os"] == "DEBUG only handler"


def test_specific_modules_single_str_module():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    with pytest.raises(TypeError, match="module A must be a ModuleType.") as e:
        _specific_modules(config, "Ash", "DEBUG")


def test_specific_modules_multiple_str_module():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    with pytest.raises(TypeError, match="module Ash must be a ModuleType.") as e:
        _specific_modules(config, ["Ash", "Birch"], "DEBUG")


def test_logging_disabled():
    from felling.src.configure_felling import configure
    import sys

    print(sys.version_info)
    if sys.version_info.minor <= 6:
        logging.disable(50)
    else:
        logging.disable()

    log_path = "./tests/logs"
    shutil.rmtree(log_path, ignore_errors=True)

    configure()
    assert os.path.isdir(log_path) is False
