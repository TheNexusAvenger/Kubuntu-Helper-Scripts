"""
TheNexusAvenger

Installs a program or programs though apt.
"""

from Step.Standard.RunProcess import runProcessStep
from typing import Callable, List


def installAptStep(programs: List[str]) -> Callable:
    """Step for installing a program or programs from apt.

    :param programs: Program or programs to install.
    :return: Callable for running the step.
    """

    aptInstallArguments = ["apt", "install", "-y"]
    aptInstallArguments.extend(programs)
    return runProcessStep(aptInstallArguments)