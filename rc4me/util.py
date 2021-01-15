import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def copyfiles(source_dir: str, destination_dir: str):
    """Copy files from source to (hidden) destination

    Example filesystem:
        dir1/
            bashrc

    copyfiles("dir1", "dir2")

    Output:
        dir1/
            bashrc
        dir2/
            .bashrc

    Args:
        source_dir: source directory
        destination_dir: destination directory
    """
    source_path = Path(source_dir)
    destin_path = Path(destination_dir)
    logger.info(f"Moving files from {source_path} to {destin_path}")
    for f in source_path.glob("*"):
        new_path = destin_path / f".{f.name}"
        logger.info(f"Moving {f}->{new_path}")
        shutil.copy(f, new_path)
