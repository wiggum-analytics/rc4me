from pathlib import Path
from click.testing import CliRunner
from rc4me.run import cli


def test_pass():
    """ Temp test before any written"""
    pass


def check_repo_files_in_home(repo: Path):
    home_rcs = [f.name for f in Path("~").expanduser().glob(".*")]
    for f in repo.glob("*"):
        if f.is_file() and f.suffix != ".md":
            assert f".{f.name}" in home_rcs


def test_get():
    runner = CliRunner()
    result = runner.invoke(cli, ["get", "jeffmm/vimrc"])
    assert result.exit_code == 0
    repo = Path("~/.rc4me/jeffmm/vimrc").expanduser()
    assert repo.exists()
    assert repo.is_dir()
    check_repo_files_in_home(repo)


def test_revert():
    pass


def test_reset():
    pass


def test_get_local():
    pass
