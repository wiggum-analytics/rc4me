"""TODO - Docstring."""

from pathlib import Path
from typing import Optional, Dict
import logging
import click

from rc4me.util import RcDirs


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.group()
# Allow calling function without an argument for --revert or --reset options
@click.option("--dest", type=click.Path())
@click.option("--home", type=click.Path())
@click.pass_context
def cli(
    ctx: Dict[str, RcDirs],
    home: Optional[str] = None,
    dest: Optional[str] = None,
) -> None:
    """Management for rc4me run commands."""
    # If the command was called without any arguments or options
    ctx.ensure_object(dict)
    if home is None:
        home = Path.home() / ".rc4me"
    else:
        home = Path(home)
    if dest is None:
        dest = Path.home()
    else:
        dest = Path(dest)

    ctx.obj["rc_dirs"] = RcDirs(home, dest)


@click.argument("repo", required=True, type=str)
@cli.command()
@click.pass_context
def get(ctx: Dict[str, RcDirs], repo: str):
    """Switch rc4me environment to target repo.

    Replaces rc files in rc4me home directory with symlinks to files located in
    target repo. If the target repo does not exist in the rc4me home directory,
    the repo is cloned either locally or from GitHub.

    Args:
        repo: Target repo with rc files. May be a local repo or reference a
            GitHub repository (e.g. jeffmm/vimrc).
    """
    rc_dirs = ctx.obj["rc_dirs"]
    # Init repo variables
    logger.info(f"Getting and setting rc4me config: {repo}")
    # Clone repo to rc4me home dir or update existing local config repo
    rc_dirs.fetch_repo(repo)
    # Wait to relink current until after _fetch_repo, since it could fail if
    # the git repo doesn't exist or similar.
    rc_dirs.change_current_to_target(rc_dirs.repo)
    # Link rc4me target config to destination
    rc_dirs.link_files()


@cli.command()
@click.pass_context
def revert(ctx: Dict[str, RcDirs]):
    """Revert to previous rc4me configuration.

    Removes changes from most recent rc4me command and reverts to previous
    configuration.
    """
    # Init rc4me directory variables
    rc_dirs = ctx.obj["rc_dirs"]
    logger.info("Reverting rc4me config to previous configuration")
    rc_dirs.change_current_to_target(rc_dirs.prev.resolve())
    # Link rc4me target config to destination
    rc_dirs.link_files()


@cli.command()
@click.pass_context
def reset(ctx: Dict[str, RcDirs]):
    """Reset to initial rc4me configuration.

    Restores the rc4me destination directory rc files to the user's initial
    configuration. If any files were overwritten by rc4me at any point, they
    will be copied back into the rc4me destination directory.
    """
    # Init rc4me directory variables
    rc_dirs = ctx.obj["rc_dirs"]
    logger.info("Restoring rc4me config to initial configuration")
    rc_dirs.change_current_to_target(rc_dirs.init)
    # Link rc4me target config to destination
    rc_dirs.link_files()


if __name__ == "__main__":
    cli()
