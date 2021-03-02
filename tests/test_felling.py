import os
from pathlib import Path
import shutil


def test_configure_default_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = "./tests/logs"
    configure()

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_str_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = "./tests/logs"
    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_pathlib_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = Path("./tests/logs")
    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)
