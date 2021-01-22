"""Utility classes and functions for rc4me."""

import logging
import shutil
from pathlib import Path
import git


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RcDirs:
    """Class for storing and manipulating rc4me home directory structure."""

    def __init__(self, rc4me_home: Path, rc4me_dest: Path):
        """Initialize paths to home and source rc4me config repos.

        Creates attributes `source`, which is the path to the
        local config repo that will be copied to the user's target
        directory.

        Args:
            rc4me_home: Path to rc4me home directory.
            rc4me_dest: Directory to copy rc files to.
        """
        # Directory that holds all cloned rc config repos, and init, prev, current
        self.home = rc4me_home
        # Directory to copy rc4me files to (e.g. $HOME)
        self.dest = rc4me_dest
        # Init rc4me home dir variables (init, prev, current)
        self._init_rc4me_home()
        # Initialize repo variables
        self.repo = None
        self.source = None
        self.repo_is_local = None

    def set_repo(self, repo: str):
        """Set repo path to clone."""
        # Git/local repo from which to clone rc config
        self.repo = repo
        self.repo_is_local = Path(self.repo).expanduser().exists()
        # Init self.source attribute, which will be the path to local repo in
        # rc4me_home with target config
        if self.repo_is_local:
            self.repo = str(Path(self.repo).expanduser())
            self.source = self.home / Path(self.repo).name
        else:
            self.source = self.home / self.repo

    def relink_current_to(self, target: Path):
        """Change current symlink to point to target path."""
        # Update prev symlink to point to current
        self.prev.unlink()
        self.prev.symlink_to(self.current.resolve())
        # Update current to point to target
        self.current.unlink()
        self.current.symlink_to(target)

    def _init_rc4me_home(self):
        """Create rc4me directory variables w/ init, prev, and current config.

        This function creates the rc4me home directory path
        variables and scaffolds the directory if necessary.  The
        `init` directory should contain all non-symlinked files
        that would otherwise be overwritten by rc4me. The `prev`
        and `current` are symlinked directories that point to the
        user's previous and current rc4me config directories,
        respectively, initially linked to `init` at creation.
        """
        self.init = self.home / "init"
        self.prev = self.home / "prev"
        self.current = self.home / "current"
        # If this is the first time calling rc4me, scaffold rc4me home dir
        if not self.init.exists():
            # Allow this to fail if home parent dir doesn't
            # exist (the home dir itself may already exist if
            # the user specified --home with an existing dir)
            self.home.mkdir(exist_ok=True)
            self.init.mkdir()
            self.prev.symlink_to(
                self.init,
            )
            self.current.symlink_to(self.init)


def link_files(rc_dirs: RcDirs):
    """Link files from rc4me source to (hidden) destination.

    Transfers files found in the rc4me source directory and
    creates symlinks of them in the rc4me destination
    directory. If the source directory is rc4me_home/init,
    the files are copied instead, allowing a user to safely
    delete their rc4me home dir after a reset.

    Args:
        rc_dirs: Data structure with rc4me home directory organization variables.
    """
    source_path = rc_dirs.current
    destin_path = rc_dirs.dest
    # If we are restoring the initial config, copy the files rather than
    # link them, so that the user can safely delete their rc4me home dir
    copy_files = source_path.resolve() == rc_dirs.init
    for f in source_path.glob("*"):
        # Skip copying any directories or README files for now (stop-gap)
        # TODO -- add ability to copy/link directories
        if f.is_dir() or "README" in f.name:
            continue
        new_path = destin_path / f".{f.name}"
        # Unlink any files that exist at new_path
        if new_path.exists():
            # If we would be overwriting a non-symlinked file, copy to rc4me_home/init
            if not new_path.is_symlink():
                backup_path = rc_dirs.init / f"{f.name}"
                logger.info(f"Backing up {new_path}->{backup_path}")
                shutil.copy(new_path, backup_path)
            # Unlink the existing file
            new_path.unlink()
        if copy_files:
            # Copy the files from the source to the new path -- only occurs
            # when source is rc4me_home/init
            logger.info(f"Moving {f}->{new_path}")
            shutil.copy(f, new_path)
        else:
            # Symlink the source rc files to the new path (syntax on this is
            # opposite the copy syntax, which may lead to confusion...)
            logger.info(f"Linking {new_path}->{f}")
            new_path.symlink_to(f)


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
