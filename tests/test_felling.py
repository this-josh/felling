import os
import shutil


def test_configure_default_path():
    """Quick sanity check test"""
    from felling import configure

    log_path = "./tests/logs"
    configure()

    assert len(os.listdir(log_path)) == 1
    shutil.rmtree(log_path)
