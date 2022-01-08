"""
TheNexusAvenger

Installs a Debian .deb file.
"""

from Step.Standard.RunProcess import runProcess
from typing import Callable


def installDebFile(path: str) -> None:
    """Installs a .deb file.

    :param path: Path to the .deb file.
    """

    try:
        # Install the .deb file.
        runProcess(["dpkg", "-i", path])
    except:
        # Install the dependencies after it fails and try again.
        runProcess(["apt", "-f", "install", "-y"])
        runProcess(["dpkg", "-i", path])

def installDebFileStep(path: str) -> Callable:
    """Step for installing a .deb package.

    :param path: Path to the .deb file.
    :return: Callable for running the step.
    """

    return lambda: installDebFile(path)