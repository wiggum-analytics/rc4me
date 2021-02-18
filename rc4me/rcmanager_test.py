from pathlib import Path

from rc4me.rcmanager import RcManager


def test_init():
    """Check initialization of path properties in RcDirs."""
    dest = Path.home()
    home = Path.home() / ".rc4me"
    rcd = RcManager(home, dest)
    assert rcd.home == home
    assert rcd.dest == dest
    assert rcd.repo_path is None
    assert rcd._current_is_init()


def test_rcmanager_get_rc_repo(tmp_path, rc1, rc2):
    rcmanager = RcManager(tmp_path, "./")
    found_rcs = rcmanager.get_rc_repos()
    expected_rcs = {rc1.name: rc1, rc2.name: rc2, "init": tmp_path / "init"}
    assert found_rcs == expected_rcs
