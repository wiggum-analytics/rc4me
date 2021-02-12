from pathlib import Path
import pytest
from rc4me.util import RcDirs


@pytest.fixture()
def rcd():
    dest = Path.home()
    home = Path.home() / ".rc4me"
    return RcDirs(home, dest)


def test_init(rcd):
    """Check initialization of path properties in RcDirs."""
    assert rcd.home == Path.home() / ".rc4me"
    assert rcd.dest == Path.home()
    assert rcd.repo_path is None
    assert rcd._current_is_init()
