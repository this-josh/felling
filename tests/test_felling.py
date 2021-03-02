import os
from pathlib import Path
import shutil


def test_configure_default_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = "./tests/logs"
    shutil.rmtree(log_path, ignore_errors=True)

    configure()

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_str_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = "./tests/logs_str"
    shutil.rmtree(log_path, ignore_errors=True)

    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)


def test_configure_pathlib_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = Path("./tests/logs_path")
    shutil.rmtree(log_path, ignore_errors=True)

    configure(log_path)

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)

def test_configure_file_name():
    """Check custom file names are working"""
    from felling import configure
    import re
    log_path = Path("./tests/logs")
    shutil.rmtree(log_path, ignore_errors=True)
    file_name = 'test_log'
    configure(log_path, log_file_name=file_name)

    assert len(os.listdir(log_path)) == 1

    assert re.match(r'^[0-9]{6}-[0-9]{4}_'+file_name+'.log', os.listdir(log_path)[0]) is not None

    shutil.rmtree(log_path)
