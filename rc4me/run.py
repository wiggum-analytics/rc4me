"""TODO - Docstring."""

import sys
from pathlib import Path
from typing import Optional
import logging
import click

from rc4me.util import RcDirs, link_files
from rc4me.prepare_repo import prepare_repo

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
# Allow calling function without an argument for --revert or --reset options
@click.argument("repo", required=False, type=str)
@click.option("--dest", type=click.Path())
@click.option("--home", type=click.Path())
@click.option("--revert", is_flag=True)
@click.option("--reset", is_flag=True)
def cli(
    repo: Optional[str] = None,
    home: Optional[str] = None,
    dest: Optional[str] = None,
    revert: bool = False,
    reset: bool = False,
) -> None:
    """Fetch dotfile repo and link rc files to destination."""
    # If the command was called without any arguments or options
    if repo is None and not (revert or reset):
        # TODO--Show user help
        logger.warning(f"Usage: {sys.argv[0]} [options] <repo_name>")
        sys.exit(1)
    # Set up defaults
    if home is None:
        home = Path.home() / ".rc4me"
    else:
        home = Path(home)
    if dest is None:
        dest = Path.home()
    else:
        dest = Path(dest)
    # Init rc4me directory variables
    rc_dirs = RcDirs(repo, home, dest)
    # Clone repo to rc4me home dir or update existing local config repo
    prepare_repo(rc_dirs, revert, reset)
    # Link rc4me target config to destination
    link_files(rc_dirs)


if __name__ == "__main__":
    cli()
