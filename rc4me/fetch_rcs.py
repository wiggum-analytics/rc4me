"""Clone dotfile repo to rc4me home directory."""

from pathlib import Path
import logging
import click
import git

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("rc4me_home", type=click.Path())
@click.argument("repo", type=str)
def _fetch_rcs_cli(rc4me_home: str, repo: str) -> None:
    """CLI wrapper for fetch_rcs function.

    Args:
        rc4me_home: Location of rc4me home directory (e.g. ~/.rc4me).
        repo: Local repo or GitHub repo stub (e.g. "jeffmm/vimrc").

    Returns:
        None

    """
    fetch_rcs(Path(rc4me_home), repo)


def fetch_rcs(rc4me_home: Path, repo: str) -> None:
    """Clone RC repository to local directory.

    Clones rc4me repository to rc4me home directory at $HOME/.rc4me. If the
    repo already exists locally, fetch updates and confirm update to origin
    master. If the .rc4me home directory does not exist, scaffold it.

    Args:
        rc4me_home: Location of rc4me home directory (e.g. ~/.rc4me).
        repo: Local repo or GitHub repo stub (e.g. "jeffmm/vimrc").

    Returns:
        None

    """
    repo_dir = rc4me_home / repo
    # Check if the rc4me home directory exists, and if not, scaffold it
    if not rc4me_home.exists():
        init_rc4me(rc4me_home)
    # First check whether the repo is already cloned in the home directory
    if repo_dir.exists():
        # If the repo already exists, fetch and update
        fetch_info = git.Repo(repo_dir).remote("origin").fetch()
        # Check that the repo is up to date
        if fetch_info[0].commit.hexsha != git.Repo(repo_dir).head.commit.hexsha:
            # Update on user confirmation
            if _check_if_overwrite(repo):
                git.Repo(repo_dir).remote("origin").pull("master")
    # If it's not already in the home directory, check if the source directory refers to
    # a local directory
    elif Path(repo).exists():
        # If the path refers to a local directory, assume the directory is a git repo
        git.Repo.clone(repo, repo_dir, branch="master", depth=1)
    # It's not there and it's not a local directory, so assume it is a GitHub repo
    else:
        # Clone from GitHub to the rc4me_home directory
        git.Repo.clone_from(
            f"https://github.com/{repo}", repo_dir, branch="master", depth=1
        )


def _check_if_overwrite(repo: str) -> bool:
    """Get user confirmation to pull new changes to rc repo."""
    confirm = input(f"Repository {repo} has new updates. Pull repo changes? (y/N): ")
    return confirm.lower() == "y"


def init_rc4me(rc4me_home: Path) -> None:
    """Scaffold rc4me directory w/ init config, symlinks to current and prev configs.

    This function creates the rc4me home directory and creates one new
    directory and two symlinked directories. The `init` directory should
    contain all non-symlinked files that would otherwise be overwritten by
    rc4me. The `prev` and `current` are symlinked directories that point to the
    user's previous and current rc4me configs, respectively, initialized to
    link to `init`.

    Args:
        rc4me_home: Path to rc4me home folder.

    Returns:
        None

    """
    # Allow this to fail if e.g. parent dir doesn't exist
    rc4me_home.mkdir()
    Path(rc4me_home / "init").mkdir()
    Path(rc4me_home / "prev").symlink_to(rc4me_home / "init")
    Path(rc4me_home / "current").symlink_to(rc4me_home / "init")


if __name__ == "__main__":
    _fetch_rcs_cli()
