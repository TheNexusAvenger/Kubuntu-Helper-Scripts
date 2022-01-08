"""
TheNexusAvenger

Step for downloading a file.
"""

import os
import requests
from typing import Callable


def getDownloadLocation(fileName: str) -> str:
    """Returns the path for a file to download.

    :param fileName: File name to ge the path for.
    :return: Full path of the file.
    """

    return os.path.realpath(os.path.join("/tmp", fileName))


def downloadFile(url: str, fileName: str) -> None:
    """Downloads a file.

    :param url: URL of the file.
    :param fileName: Name of the file to download.
    """

    # Get the download location.
    filePath = getDownloadLocation(fileName)
    if os.path.exists(filePath):
        print("Already downloaded " + fileName)
        return

    # Download the file.
    print("Downloading " + fileName + " from " + url)
    with open(filePath, "wb") as file:
        file.write(requests.get(url).content)


def downloadFileStep(url: str, fileName: str) -> Callable:
    """Creates a step for downloading a file.

    :param url: URL of the file.
    :param fileName: Name of the file to download.
    :return: Callable for the step.
    """

    return lambda: downloadFile(url, fileName)