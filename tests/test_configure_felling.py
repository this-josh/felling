import os
from pathlib import Path
import shutil
import pytest


def test_configure_default_path():
    """Quick sanity check test"""
    from felling.src.configure_felling import configure

    log_path = "./tests/logs"
    shutil.rmtree(log_path, ignore_errors=True)

    configure()

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


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
    import re

    log_path = Path("./tests/logs")
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
    import re

    config = {"handlers": {"file_handler": {"filename": "NOT A FILENAME"}}}
    log_path = Path("./logs")
    log_file_name = "test_file_name"
    expected_path = log_path / (log_file_name + ".log")
    config = _update_filenames(config, log_file_name, log_path)
    assert (
        re.match(
            r"^[0-9]{8}-[0-9]{4}_" + log_file_name + ".log",
            config["handlers"]["file_handler"]["filename"].name,
        )
        is not None
    )


def test_get_git_commit_hash():
    from felling.src.configure_felling import _get_git_commit_hash
    import re

    commit_hash = _get_git_commit_hash()

    assert isinstance(commit_hash, str)

    assert re.match(r"\b[0-9a-f]{5,40}\b", commit_hash)


@pytest.fixture()
def _mocked_get_git_commit_hash(mocker):
    mocker.patch(
        "felling.src.configure_felling.subprocess.check_output",
        return_value="str does not have decode",
    )


def test_get_git_commit_hash(_mocked_get_git_commit_hash):
    from felling.src.configure_felling import _get_git_commit_hash

    commit_hash = _get_git_commit_hash()

    assert commit_hash is None


def test_get_git_branch_and_remote():
    from felling.src.configure_felling import _get_git_branch_and_remote

    git_branch_and_remote = _get_git_branch_and_remote()

    assert isinstance(git_branch_and_remote, str)

    # 13 on my machine, 11 on github action, for now just check greater than 10
    assert git_branch_and_remote.count("\n") > 10


def test_initial_logs():
    from felling.src.configure_felling import _initial_logs

    _initial_logs()


def test_log_versions_no_package():
    from felling.src.configure_felling import _log_versions

    assert _log_versions(None) is None


def test_log_versions_one_package():
    from felling.src.configure_felling import _log_versions
    import felling

    assert _log_versions(felling) is None


def test_log_versions_multiple_package():
    from felling.src.configure_felling import _log_versions
    import felling
    import re

    assert _log_versions((felling, re)) is None


def test_log_versions_invalid_package():
    from felling.src.configure_felling import _log_versions
    import os

    assert _log_versions(os) is None


def test_log_versions_other_error():
    from felling.src.configure_felling import _log_versions

    # 3 gives SyntaxError
    assert _log_versions(3) is None


def test_specific_modules_one_module_error_only():
    from felling.src.configure_felling import _specific_modules
    import re

    config = {"loggers": {"ERROR only": "ERROR only handler"}}
    config = _specific_modules(config, re, "ERROR")
    assert config["loggers"]["re"] == "ERROR only handler"


def test_specific_modules_multiple_module_error_only():
    from felling.src.configure_felling import _specific_modules
    import re
    import os

    config = {"loggers": {"ERROR only": "ERROR only handler"}}
    config = _specific_modules(config, [re, os], "ERROR")
    assert config["loggers"]["re"] == "ERROR only handler"
    assert config["loggers"]["os"] == "ERROR only handler"


def test_specific_modules_one_module_debug_only():
    from felling.src.configure_felling import _specific_modules
    import re

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    config = _specific_modules(config, re, "DEBUG")
    assert config["loggers"]["re"] == "DEBUG only handler"


def test_specific_modules_multiple_module_debug_only():
    from felling.src.configure_felling import _specific_modules
    import re
    import os

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    config = _specific_modules(config, [re, os], "DEBUG")
    assert config["loggers"]["re"] == "DEBUG only handler"
    assert config["loggers"]["os"] == "DEBUG only handler"


def test_specific_modules_single_str_module():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    with pytest.raises(TypeError) as e:
        config = _specific_modules(config, "Ash", "DEBUG")


def test_specific_modules_multiple_str_module():
    from felling.src.configure_felling import _specific_modules

    config = {"loggers": {"DEBUG only": "DEBUG only handler"}}
    with pytest.raises(TypeError) as e:
        config = _specific_modules(config, ["Ash", "Birch"], "DEBUG")


def test_logging_disabled():
    import logging
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