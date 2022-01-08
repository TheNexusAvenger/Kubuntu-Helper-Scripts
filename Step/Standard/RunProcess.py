"""
TheNexusAvenger

Runs a process and waits for it to complete.
"""

import subprocess
from typing import Callable, List


def runProcess(parameters: List[str], workingDirectory: str = None) -> None:
    """Runs a process.

    :param parameters: Parameters to run in the process, including the file and parameters to the file.
    :param workingDirectory: Working directory to run the process.
    """

    process = subprocess.Popen(parameters, cwd=workingDirectory)
    process.wait()
    if process.returncode != 0:
        raise Exception("Process returned an error code " + str(process.returncode))


def runProcessStep(parameters: List[str], workingDirectory: str = None) -> Callable:
    """Creates a step for running a process.

    :param parameters: Parameters to run in the process, including the file and parameters to the file.
    :param workingDirectory: Working directory to run the process.
    :return: Callable for the step.
    """

    return lambda: runProcess(parameters, workingDirectory)
