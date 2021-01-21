"""Utility classes and functions for rc4me."""

import logging
import shutil
from typing import Optional
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RcDirs:
    """Class for common rc4me data, like home directory, etc."""

    def __init__(
        self, target_config: Optional[str], rc4me_home: Path, rc4me_dest: Path
    ):
        """Initialize paths to home and source rc4me config repos.

        Creates attributes `source`, which is the path to the
        local config repo that will be copied to the user's target
        directory.

        Args:
            rc4me_home: Path to rc4me home directory. If None,
                variables are initialized, but no repos are cloned
                or updated.
            target_config: Path to local rc repo or remote rc repo name
            rc4me_dest: Directory to copy rc files to.
        """
        # Directory that holds all cloned rc config repos, and init, prev, current
        self.home = rc4me_home
        # Git/local repo from which to clone rc config
        self.target = target_config
        # Directory to copy rc4me files to (e.g. $HOME)
        self.dest = rc4me_dest
        # Init rc4me home dir variables (init, prev, current)
        self._init_rc4me_home()
        if self.target is None:
            return
        self.target_is_local = Path(self.target).expanduser().exists()
        # Init self.source attribute, which will be the path to local repo in
        # rc4me_home with target config
        if self.target_is_local:
            self.target = str(Path(self.target).expanduser())
            self.source = self.home / Path(self.target).name
        else:
            self.source = self.home / self.target

    def relink_current_to(self, target: Path):
        """Change current symlink to point to target."""
        self.prev.unlink()
        self.prev.symlink_to(self.current.resolve())
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
    # Prefer revert over reset if both flags were given
    destin_path = rc_dirs.dest
    # If we are restoring the initial config, copy the files rather than
    # link them, so that the user can safely delete their rc4me home dir
    copy_files = source_path.resolve() == rc_dirs.init
    logger.info(f"Moving files from {source_path} to {destin_path}")
    for f in source_path.glob("*"):
        # Skip copying the .git directory and README file (stop-gap)
        if f.name == ".git" or "README" in f.name:
            continue
        new_path = destin_path / f".{f.name}"
        # Unlink any files being referenced
        if new_path.exists():
            # If we would be overwriting a non-symlinked file, copy to rc4me_home/init
            if not new_path.is_symlink():
                backup_path = rc_dirs.init / f"{f.name}"
                logger.info(f"Backing up {new_path}->{backup_path}")
                shutil.copy(new_path, backup_path)
            new_path.unlink()
        if copy_files:
            logger.info(f"Moving {f}->{new_path}")
            shutil.copy(f, new_path)
        else:
            # Symlink the source rc files to the new path
            # The syntax on this is opposite the copy syntax, which may be confusing...
            logger.info(f"Linking {new_path}->{f}")
            new_path.symlink_to(f)
