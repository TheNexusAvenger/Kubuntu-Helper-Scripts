"""
TheNexusAvenger

Step for downloading an archive.
"""

import os
import tarfile
import zipfile
from typing import Callable
from Step.Standard.DownloadFile import getDownloadLocation, downloadFile


def downloadArchive(url: str, extension: str, fileName: str) -> None:
    """Downloads and extracts an archive.

    :param url: URL of the file.
    :param extension: Extension of the archive.
    :param fileName: Name of the file to download.
    """

    # Get the download and extract locations.
    archivePath = getDownloadLocation(fileName + "." + extension)
    extractPath = getDownloadLocation(fileName)
    if os.path.exists(extractPath):
        print("Already extracted " + fileName)
        return

    # Download the file.
    print("Downloading " + fileName + " from " + url)
    downloadFile(url, fileName + "." + extension)

    # Extract the file.
    print("Extracting " + fileName)
    if extension.lower() == "tar.gz":
        file = tarfile.open(archivePath)
        file.extractall(extractPath)
        file.close()
    elif extension.lower() == "zip":
        file = zipfile.ZipFile(archivePath)
        file.extractall(extractPath)
        file.close()


def downloadArchiveStep(url: str, extension: str, fileName: str) -> Callable:
    """Creates a step for downloading a file.

    :param url: URL of the file.
    :param extension: Extension of the archive.
    :param fileName: Name of the file to download.
    :return: Callable for the step.
    """

    return lambda: downloadArchive(url, extension, fileName)