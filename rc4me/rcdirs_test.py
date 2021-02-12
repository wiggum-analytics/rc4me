from pathlib import Path
from rc4me.util import RcDirs


def test_init():
    """TODO"""
    dest = Path.home()
    home = dest / ".rc4me"
    rcd = RcDirs(home, dest)
    assert rcd.home == home
    assert rcd.dest == dest
