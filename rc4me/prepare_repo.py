"""Functions for initializing and updating rc4me repo."""

import logging

import git

from rc4me.rcmanager import RcManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def prepare_repo(
    rcmanager: RcManager, revert: bool = False, reset: bool = False
) -> None:
    """Prepare rc repository to copy to rc4me destination.

    Configures links to previous and current rc4me configs.

    Args:
        rcmanager: Data for rc home directory and rc4me target config.
        revert: Flag to revert changes to prev rc4me config
        reset: Flag to reset changes to init rc4me config

    Returns:
        None
    """
    # Resolve symlinks and remove them
    # Prefer to revert over reset in case both flags are given for some reason
    if revert:
        logger.info("Reverting rc4me config to previous configuration")
        rcmanager.relink_current_to(rcmanager.prev.resolve())
    elif reset:
        logger.info("Restoring rc4me config to initial configuration")
        rcmanager.relink_current_to(rcmanager.init)
    else:
        _fetch_repo(rcmanager)
        # Wait to relink current until after _fetch_repo, since it could fail if
        # the git repo doesn't exist or similar.
        rcmanager.relink_current_to(rcmanager.source)


def _fetch_repo(rcmanager: RcManager) -> None:
    """Clone RC repository to local directory.

    Clones rc4me repository to rc4me home directory at $HOME/.rc4me. If the
    repo already exists locally, fetch updates and confirm update to origin
    master. If the .rc4me home directory does not exist, scaffold it.

    Args:
        rcmanager: Data for rc home directory and rc4me target config.

    Returns:
        None
    """

    def _check_if_overwrite() -> bool:
        """Get user confirmation to pull new changes to rc repo."""
        confirm = input(
            f"Repository {rcmanager.target} has new updates. Pull changes? (y/N): "
        )
        return confirm.lower() == "y"

    # First check whether the repo is already cloned in the home directory
    if rcmanager.source.exists():
        repo = git.Repo(rcmanager.source)
        # Fetch any changes from origin
        fetch_info = repo.remote("origin").fetch()
        # Check that the local repo is up to date
        if fetch_info[0].commit.hexsha != repo.head.commit.hexsha:
            # Update the repo on user confirmation
            if _check_if_overwrite():
                repo.remote("origin").pull("master")
    # If the target is a local directory, clone from the local directory
    elif rcmanager.target_is_local:
        # If the path refers to a local directory, assume the directory is a git repo
        logger.info(f"Cloning directory {rcmanager.target}")
        git.Repo(rcmanager.target).clone(rcmanager.source, branch="master", depth=1)
    # Otherwise assume the target refers to a remote GitHub repository
    else:
        # Clone from GitHub to the rc4me_home directory
        logger.info(f"Cloning GitHub repo {rcmanager.target}")
        git.Repo.clone_from(
            f"https://github.com/{rcmanager.target}",
            rcmanager.source,
            branch="master",
            depth=1,
        )
