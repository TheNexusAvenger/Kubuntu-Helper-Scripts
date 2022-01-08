"""
TheNexusAvenger

Installs Nexus LU Launcher.
"""

import os
import requests
import shutil
import stat
from Step.Standard.DownloadArchive import downloadArchive
from Step.Standard.DownloadFile import getDownloadLocation


def installNexusLULauncher() -> None:
    # Download the archive.
    nlulArchiveLocation = getDownloadLocation("nlul")
    if not os.path.exists(nlulArchiveLocation):
        latestTag = requests.get("https://github.com/TheNexusAvenger/Nexus-LU-Launcher/releases/latest", headers={"Accept": "application/json"}).json()["tag_name"]
        downloadArchive("https://github.com/TheNexusAvenger/Nexus-LU-Launcher/releases/download/" + latestTag + "/Nexus-LU-Launcher-Linux-x64.zip", "zip", "nlul")

    # Copy the files.
    nlulLocation = os.path.expanduser("~/.local/share/nexus-lu-launcher/")
    if not os.path.exists(nlulLocation):
        os.makedirs(nlulLocation)
    for fileName in os.listdir(nlulArchiveLocation):
        newFileLocation = os.path.join(nlulLocation, fileName)
        if os.path.exists(newFileLocation):
            os.remove(newFileLocation)
        shutil.copy(os.path.join(nlulArchiveLocation, fileName), newFileLocation)

    # Make Nexus LU Launcher executable.
    executableLocation = os.path.join(nlulLocation, "Nexus-LU-Launcher")
    executableStat = os.stat(executableLocation)
    os.chmod(executableLocation, executableStat.st_mode | stat.S_IEXEC)

    # Download the icon.
    iconLocation = os.path.join(nlulLocation, "NexusLULauncherLogo.png")
    if not os.path.exists(iconLocation):
        with open(iconLocation, "wb") as file:
            file.write(requests.get("https://raw.githubusercontent.com/TheNexusAvenger/Nexus-LU-Launcher/master/NLUL.GUI/Assets/Images/NexusLegoUniverseLauncherLogo.png").content)

    # Create the desktop file.
    desktopFileLocation = os.path.expanduser("~/.local/share/applications/nexus-lu-launcher.desktop")
    if not os.path.exists(desktopFileLocation):
        with open(desktopFileLocation, "w") as file:
            file.write("[Desktop Entry]\r\n")
            file.write("Version=1.0\r\n")
            file.write("Type=Application\r\n")
            file.write("Name=Nexus LU Launcher\r\n")
            file.write("Icon=" + iconLocation + "\r\n")
            file.write("Exec=" + executableLocation + "\r\n")
            file.write("Categories=Game;")
