import subprocess
import sys

from i10_bluesky import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "i10_bluesky", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
