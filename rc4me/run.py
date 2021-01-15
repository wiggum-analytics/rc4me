"""TODO - Docstring."""

from pathlib import Path
from typing import Optional
import logging
import click

from rc4me.fetch_rcs import fetch_rcs
from rc4me.util import copyfiles

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

RC4ME_HOME = Path.home() / ".rc4me"


@click.command()
@click.argument("repo", type=str)
@click.argument("dest", required=False, type=str)
def cli(repo: str, dest: Optional[str] = None) -> None:
    """Fetch dotfile repo and link rc files to destination."""
    # Check if the config is already downloaded, and if not, clone to rc4me home dir
    fetch_rcs(RC4ME_HOME, repo)
    # Copy rc4me target config to destination (assume home directory for now)
    if dest is None:
        dest = str(Path.home())
    copyfiles(RC4ME_HOME / repo, dest)


if __name__ == "__main__":
    cli()
