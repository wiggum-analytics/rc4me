"""Utility classes and functions for rc4me."""

import logging
import shutil
from pathlib import Path
from typing import Dict

import git

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RcManager:
    """Class for storing and manipulating rc4me home directory structure."""

    def __init__(self, home: Path = Path.home() / ".rc4me", dest: Path = Path.home()):
        """Initialize paths to home and source rc4me config repos.

        Creates attributes `home`, `dest`, `repo_path`, which is the path to
        the local config repo that will be copied to the user's target
        directory.

        Args:
            home: Path to rc4me home directory.
            dest: Directory to copy rc files to.
        """
        # Directory that holds all cloned rc config repos, and init, prev, current
        self.home = home
        # Directory to copy rc4me files to (e.g. $HOME)
        self.dest = dest
        # Init rc4me home dir variables (init, prev, current)
        self._init_rc4me_home()
        # Directory holding source file repo
        self.repo_path = None

    def _current_is_init(self):
        """Check if current config is init."""
        return self.current.resolve() == self.init

    def _cleanup_links_to_current(self):
        """Remove symlinks in the home directory that link to files in current."""
        if self._current_is_init():
            # If current points to init config, then the files in current are
            # not symlinks and should not be unlinked. Real files will always be
            # copied to init if they are overwritten by a symlink.
            return
        for link, source in self._generate_link_paths():
            # For each file in the current directory, check if the file is symlinked
            # to home, and if so, unlink it from home
            if link.is_symlink() and link.resolve() == source.resolve():
                logger.info(f"Unlinking {link}")
                link.unlink()

    def _generate_link_paths(self):
        """Generate file paths to destination."""
        for source in self.current.glob("*"):
            # Skip copying any directories or README files for now (stop-gap)
            # TODO -- add ability to copy/link directories
            if source.is_dir() or "README" in source.name:
                continue
            link = self.dest / f".{source.name}"
            yield link, source

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

    def change_current_to_fetched_repo(self):
        """Change current symlink to recently-fetched repo."""
        self._update_current_and_prev_repos_and_set(self.repo_path)

    def change_current_to_prev(self):
        """Change current symlink to previous rc4me config."""
        self._update_current_and_prev_repos_and_set(self.prev.resolve())

    def change_current_to_init(self):
        """Change current symlink to initial rc4me config."""
        self._update_current_and_prev_repos_and_set(self.init)

    def change_current_to_repo(self, repo):
        """Change current symlink to passed repo rc4me config."""
        self._update_current_and_prev_repos_and_set(repo)

    def _update_current_and_prev_repos(self, target: Path):
        """Change current and previous symlink to point to target path."""
        # Fail early before we unlink anything
        if not (target and target.exists()):
            raise FileExistsError("Relink target not found.")
        self._cleanup_links_to_current()
        # Update prev symlink to point to current
        self.prev.unlink()
        self.prev.symlink_to(self.current.resolve())
        # Update current to point to target
        self.current.unlink()
        self.current.symlink_to(target)

    def _update_current_and_prev_repos_and_set(self, target: Path):
        """Runs _update_current_and_prev_repos follow by _set_repo_files"""
        self._update_current_and_prev_repos(target)
        self._set_repo_files()

    def fetch_repo(self, repo: str):
        """Clone RC repository to local directory.

        Clones rc4me repository to rc4me home directory at $HOME/.rc4me. If the
        repo already exists locally, fetch updates and confirm update from remote.

        Args:
            repo: Git/local repo from which to clone rc config
        """

        def _check_if_overwrite() -> bool:
            """Get user confirmation to pull new changes to rc repo."""
            confirm = input(f"Repository {repo} has new updates. Pull changes? (y/N): ")
            return confirm.lower() == "y"

        repo_is_local = Path(repo).expanduser().exists()
        if repo_is_local:
            repo = str(Path(repo).expanduser())
            self.repo_path = self.home / Path(repo).name
        else:
            repo_local = repo.replace("/", "_")
            self.repo_path = self.home / repo_local

        # First check whether the repo is already cloned in the home directory
        if self.repo_path.exists():
            r = git.Repo(self.repo_path)
            # Fetch any changes from origin
            fetch_info = r.remote("origin").fetch()
            # Check that the local repo is up to date
            if fetch_info[0].commit.hexsha != r.head.commit.hexsha:
                # Update the repo on user confirmation
                if _check_if_overwrite():
                    r.remote("origin").pull("master")
        # If the repo is a local directory, clone from the local directory
        elif repo_is_local:
            # If the path refers to a local directory, assume it is a git repo
            logger.info(f"Cloning directory {repo}")
            git.Repo(repo).clone(self.repo_path, branch="master", depth=1)
        # Otherwise assume the repo refers to a remote GitHub repository
        else:
            # Clone from GitHub to the home directory
            logger.info(f"Cloning GitHub repo {repo}")
            git.Repo.clone_from(
                f"https://github.com/{repo}",
                self.repo_path,
                branch="master",
                depth=1,
            )

    def _set_repo_files(self):
        """Link or copy files from rc4me source to (hidden) destination.

        Transfers files found in the rc4me source directory and creates
        symlinks of them in the rc4me destination directory. If the source
        directory is home/init, the files are copied instead, allowing a
        user to safely delete their rc4me home dir after a reset.
        """
        # If we are restoring the initial config, copy the files rather than
        # link them, so that the user can safely delete their rc4me home dir
        copy_files = self._current_is_init()
        for link_path, source_path in self._generate_link_paths():
            # Unlink any files that exist at link_path
            if link_path.exists():
                # If we would be overwriting a non-symlinked file, copy to init
                if not link_path.is_symlink():
                    backup_path = self.init / f"{source_path.name}"
                    logger.info(f"Backing up {link_path}->{backup_path}")
                    shutil.copy(link_path, backup_path)
                # Unlink the existing file
                link_path.unlink()
            # Copy files if we are changing config to init.
            if copy_files:
                logger.info(f"Copying {source_path}->{link_path}")
                shutil.copy(source_path, link_path)
            else:
                # Symlink the source rc files to the new path.
                logger.info(f"Linking {source_path}->{link_path}")
                link_path.symlink_to(source_path)

    def get_rc_repos(self) -> Dict[str, Path]:
        """Searches home dir and grabs all the rc repos it finds

        Excludes "current" and "prev".

        Returns:
            Map with key repo name, value repo Path
        """
        dirs = [p for p in self.home.glob("*") if p.name not in ["current", "prev"]]
        return {p.name: p for p in dirs}
