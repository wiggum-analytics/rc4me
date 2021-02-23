from pathlib import Path

from click.testing import CliRunner

from rc4me.cli import cli


def check_repo_files_in_home(repo: Path):
    """Check that files in a repo are in the rc4me destination dir."""
    home_rcs = [f.name for f in Path("~").expanduser().glob(".*")]
    for f in repo.glob("*"):
        if f.is_file() and f.suffix != ".md":
            assert f".{f.name}" in home_rcs


def test_apply():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "jeffmm/vimrc"])
    assert result.exit_code == 0
    repo = Path("~/.rc4me/jeffmm_vimrc").expanduser()
    assert repo.exists()
    assert repo.is_dir()
    check_repo_files_in_home(repo)


def test_revert():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "mstefferson/rc-demo"])
    assert result.exit_code == 0
    ms_repo = Path("~/.rc4me/mstefferson_rc-demo").expanduser()
    check_repo_files_in_home(ms_repo)
    result = runner.invoke(cli, ["apply", "jeffmm/vimrc"])
    assert result.exit_code == 0
    jm_repo = Path("~/.rc4me/jeffmm_vimrc").expanduser()
    check_repo_files_in_home(jm_repo)
    result = runner.invoke(cli, ["revert"])
    assert result.exit_code == 0
    check_repo_files_in_home(ms_repo)


def test_reset():
    runner = CliRunner()
    result = runner.invoke(cli, ["apply", "mstefferson/rc-demo"])
    repo = Path("~/.rc4me/mstefferson_rc-demo").expanduser()
    assert result.exit_code == 0
    result = runner.invoke(cli, ["reset"])
    assert result.exit_code == 0
    repo = Path("~/.rc4me/init").expanduser()
    check_repo_files_in_home(repo)


def test_apply_local():
    pass
