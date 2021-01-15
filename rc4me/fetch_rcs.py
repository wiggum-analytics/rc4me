"""Clone dotfile repo to rc4me home directory."""

from pathlib import Path
import logging
import click
import git

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.argument("repo", type=str)
def _fetch_rcs_cli(rc4me_home: Path, repo: str) -> None:
    """CLI wrapper for fetch_rcs function.

    Args:
        repo: Local repo or GitHub repo stub (e.g. "jeffmm/vimrc").

    Returns:
        None

    """
    fetch_rcs(rc4me_home, repo)


def fetch_rcs(rc4me_home: Path, repo: str) -> None:
    """Clone RC repository to local directory.

    Clones rc4me repository to rc4me home directory at $HOME/.rc4me. If the
    repo already exists locally, fetch updates and confirm update to origin
    master. If the .rc4me home directory does not exist, scaffold it.

    Args:
        repo: Local repo or GitHub repo stub (e.g. "jeffmm/vimrc").

    Returns:
        None

    """
    repo_dir = rc4me_home / repo
    # Check if the repo is local first
    if not rc4me_home.exists():
        init_rc4me(rc4me_home)
    if repo_dir.exists():
        # If the repo exists, fetch and update
        fetch_info = git.Repo(repo_dir).remote("origin").fetch()
        # Check that the repo is up to date
        if fetch_info[0].commit.hexsha != git.Repo(repo_dir).head.commit.hexsha:
            # Update on user confirmation
            if _check_if_overwrite(repo):
                git.Repo(repo_dir).remote("origin").pull("master")
    else:
        # Otherwise, clone the repo
        if Path(repo).exists():
            # If the path exists locally, assume it is a git repo and clone it
            git.Repo.clone(repo, repo_dir, branch="master", depth=1)
        else:
            # Otherwise, clone it from github
            git.Repo.clone_from(
                f"https://github.com/{repo}", repo_dir, branch="master", depth=1
            )


def _check_if_overwrite(repo: str) -> bool:
    """Get user confirmation to pull new changes to rc repo."""
    confirm = input(f"Repository {repo} has new updates. Pull repo changes? (y/N): ")
    return confirm.lower() == "y"


def init_rc4me(rc4me_home: Path) -> None:
    """Scaffold rc4me directory structure.

    Args:
        rc4me_home: Path to rc4me home folder.

    Returns:
        None

    """
    # Allow this to fail if e.g. parent dir doesn't exist
    rc4me_home.mkdir()
    Path(rc4me_home / "init").mkdir()
    Path(rc4me_home / "prev").symlink_to(rc4me_home / "init")


if __name__ == "__main__":
    _fetch_rcs_cli()
