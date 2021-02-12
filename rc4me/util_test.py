from pathlib import Path
from click.testing import CliRunner
from rc4me.run import cli
from rc4me.util import RcDirs


def check_repo_files_in_home(repo: Path):
    """Check that files in a repo are in the rc4me destination dir."""
    home_rcs = [f.name for f in Path("~").expanduser().glob(".*")]
    for f in repo.glob("*"):
        if f.is_file() and f.suffix != ".md":
            assert f".{f.name}" in home_rcs


def test_get():
    runner = CliRunner()
    result = runner.invoke(cli, ["get", "mstefferson/rc-demo"])
    assert result.exit_code == 0
    repo = Path("~/.rc4me/mstefferson_rc-demo").expanduser()
    assert repo.exists()
    assert repo.is_dir()
    check_repo_files_in_home(repo)


def test_revert():
    runner = CliRunner()
    result = runner.invoke(cli, ["get", "mstefferson/rc-demo"])
    assert result.exit_code == 0
    ms_repo = Path("~/.rc4me/mstefferson_rc-demo").expanduser()
    check_repo_files_in_home(ms_repo)
    result = runner.invoke(cli, ["get", "jeffmm/vimrc"])
    assert result.exit_code == 0
    jm_repo = Path("~/.rc4me/jeffmm_vimrc").expanduser()
    check_repo_files_in_home(jm_repo)
    result = runner.invoke(cli, ["revert"])
    assert result.exit_code == 0
    check_repo_files_in_home(ms_repo)


def test_reset():
    runner = CliRunner()
    result = runner.invoke(cli, ["get", "mstefferson/rc-demo"])
    repo = Path("~/.rc4me/mstefferson_rc-demo").expanduser()
    assert result.exit_code == 0
    result = runner.invoke(cli, ["reset"])
    assert result.exit_code == 0
    repo = Path("~/.rc4me/init").expanduser()
    check_repo_files_in_home(repo)


def test_rcdirs_get_rc_repo(tmp_path, rc1, rc2):
    rcdirs = RcDirs(tmp_path, "./")
    found_rcs = rcdirs.get_rc_repos()
    expected_rcs = {rc1.name: rc1, rc2.name: rc2, "init": tmp_path / "init"}
    assert found_rcs == expected_rcs
