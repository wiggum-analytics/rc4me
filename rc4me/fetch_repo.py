"""Functions for initializing and updating rc4me repo."""

import logging
import git

from rc4me.util import RcDirs


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def fetch_repo(rc_dirs: RcDirs) -> None:
    """Clone RC repository to local directory.

    Clones rc4me repository to rc4me home directory at $HOME/.rc4me. If the
    repo already exists locally, fetch updates and confirm update to origin
    master. If the .rc4me home directory does not exist, scaffold it.

    Args:
        rc_dirs: Data for rc home directory and rc4me target config.

    Returns:
        None
    """

    def _check_if_overwrite() -> bool:
        """Get user confirmation to pull new changes to rc repo."""
        confirm = input(
            f"Repository {rc_dirs.repo} has new updates. Pull changes? (y/N): "
        )
        return confirm.lower() == "y"

    # First check whether the repo is already cloned in the home directory
    if rc_dirs.source.exists():
        repo = git.Repo(rc_dirs.source)
        # Fetch any changes from origin
        fetch_info = repo.remote("origin").fetch()
        # Check that the local repo is up to date
        if fetch_info[0].commit.hexsha != repo.head.commit.hexsha:
            # Update the repo on user confirmation
            if _check_if_overwrite():
                repo.remote("origin").pull("master")
    # If the repo is a local directory, clone from the local directory
    elif rc_dirs.repo_is_local:
        # If the path refers to a local directory, assume the directory is a git repo
        logger.info(f"Cloning directory {rc_dirs.repo}")
        git.Repo(rc_dirs.repo).clone(rc_dirs.source, branch="master", depth=1)
    # Otherwise assume the repo refers to a remote GitHub repository
    else:
        # Clone from GitHub to the rc4me_home directory
        logger.info(f"Cloning GitHub repo {rc_dirs.repo}")
        git.Repo.clone_from(
            f"https://github.com/{rc_dirs.repo}",
            rc_dirs.source,
            branch="master",
            depth=1,
        )
