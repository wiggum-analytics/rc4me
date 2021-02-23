"""TODO - Docstring."""

import logging
from pathlib import Path
from typing import Dict, Optional

import click
from pick import pick

from rc4me.rcmanager import RcManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.group()
# Allow calling function without an argument for --revert or --reset options
@click.option(
    "--dest",
    type=click.Path(),
    default=Path.home(),
    required=False,
    help=(
        "Destination path where run command files are copied/linked to. "
        "Typically home or current directory"
    ),
    show_default=True,
)
@click.pass_context
def cli(
    ctx: Dict[str, RcManager],
    dest: Optional[str] = None,
) -> None:
    """Management for rc4me run commands."""
    # If the command was called without any arguments or options
    ctx.ensure_object(dict)
    home = Path.home() / ".rc4me"
    ctx.obj["rcmanager"] = RcManager(home=home, dest=dest)


@click.argument("repo", required=True, type=str)
@cli.command()
@click.pass_context
def apply(ctx: Dict[str, RcManager], repo: str):
    """Apply rc environment. Will download from GitHub if not found in .rc4me/

    Replaces rc files in rc4me home directory with symlinks to files located in
    target repo. If the target repo does not exist in the rc4me home directory,
    the repo is cloned either locally or from GitHub.

    Args:
        repo: Target repo with rc files. May be a local repo or reference a
            GitHub repository (e.g. jeffmm/vimrc).
    """
    rcmanager = ctx.obj["rcmanager"]
    # Init repo variables
    logger.info(f"Getting and setting rc4me config: {repo}")
    # Clone repo to rc4me home dir or update existing local config repo
    rcmanager.fetch_repo(repo)
    # Wait to relink current until after fetching repo, since it could fail if
    # the git repo doesn't exist or similar.
    rcmanager.change_current_to_fetched_repo()


@cli.command()
@click.pass_context
def revert(ctx: Dict[str, RcManager]):
    """Revert to previous rc4me configuration.

    Removes changes from most recent rc4me command and reverts to previous
    configuration.
    """
    # Init rc4me directory variables
    rcmanager = ctx.obj["rcmanager"]
    logger.info("Reverting rc4me config to previous configuration")
    rcmanager.change_current_to_prev()


@cli.command()
@click.pass_context
def reset(ctx: Dict[str, RcManager]):
    """Reset to initial rc4me configuration.

    Restores the rc4me destination directory rc files to the user's initial
    configuration. If any files were overwritten by rc4me at any point, they
    will be copied back into the rc4me destination directory.
    """
    # Init rc4me directory variables
    rcmanager = ctx.obj["rcmanager"]
    logger.info("Restoring rc4me config to initial configuration")
    rcmanager.change_current_to_init()


@cli.command()
@click.pass_context
def select(ctx: Dict[str, RcManager]):
    """Select rc4me configurations.

    Displays all available repos and allow user to select one
    """
    # Init rc4me directory variables
    rcmanager = ctx.obj["rcmanager"]
    my_repos = rcmanager.get_rc_repos()
    # Show all dirs that aren't curr/prev
    title = "Please select the repo/configuration you want to use:"
    options = list(my_repos.keys())
    selected, _ = pick(options, title)
    logger.info(f"Selected and applying: {my_repos[selected]}")
    rcmanager.change_current_to_repo(my_repos[selected])


if __name__ == "__main__":
    cli()
