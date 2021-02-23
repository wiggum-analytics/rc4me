from rc4me.util import RcDirs


def test_rcdirs_get_rc_repo(tmp_path, rc1, rc2):
    rcdirs = RcDirs(tmp_path, "./")
    found_rcs = rcdirs.get_rc_repos()
    expected_rcs = {rc1.name: rc1, rc2.name: rc2, "init": tmp_path / "init"}
    assert found_rcs == expected_rcs
