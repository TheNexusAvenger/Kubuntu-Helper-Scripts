"""
TheNexusAvenger

Sets up JetBrains Toolbox.
"""

import os
from Step.Standard.DownloadFile import getDownloadLocation
from Step.Standard.DownloadArchive import downloadArchive
from Step.Standard.RunProcess import runProcess


def installJetBrainsToolbox() -> None:
    """Installs JetBrains toolbox.
    """

    # Return if JetBrains Toolbox already exists.
    if os.path.exists(os.path.expanduser("~/.local/share/JetBrains/Toolbox")):
        print("JetBrains Toolbox already installed.")
        return

    # Download JetBrains Toolbox
    downloadArchive("https://download.jetbrains.com/toolbox/jetbrains-toolbox-1.22.10970.tar.gz", "tar.gz","jetbrains-toolbox")

    # Run JetBrains Toolbox for the initial setup.
    jetBrainsExecutable = getDownloadLocation("jetbrains-toolbox")
    jetBrainsExecutable = os.path.join(jetBrainsExecutable, os.listdir(jetBrainsExecutable)[0], "jetbrains-toolbox")
    runProcess([jetBrainsExecutable])