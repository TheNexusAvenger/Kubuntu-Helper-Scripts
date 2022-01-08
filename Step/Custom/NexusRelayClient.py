"""
TheNexusAvenger

Builds and installs Nexus Relay Client.
"""

import os.path
import shutil
from Step.Standard.DownloadArchive import downloadArchive
from Step.Standard.DownloadFile import getDownloadLocation
from Step.Standard.RunProcess import runProcess


def installNexusRelayClient() -> None:
    # Return if Nexus Relay Client already exists.
    finalNexusRelayClientLocation = "/usr/local/bin/NexusRelayClient"
    if os.path.exists(finalNexusRelayClientLocation):
        print("Nexus Relay Client already exists.")
        return

    # Download Nexus Relay.
    downloadArchive("https://github.com/TheNexusAvenger/Nexus-Relay/archive/refs/heads/master.zip", "zip", "nexus-relay")

    # Build Nexus Relay Client.
    nexusRelayClientProject = os.path.join(getDownloadLocation("nexus-relay"), "Nexus-Relay-master", "NexusRelayClient")
    nexusRelayClientPublish = getDownloadLocation("nexus-relay-client")
    if not os.path.exists(nexusRelayClientPublish):
        runProcess(["dotnet", "publish", "-r", "linux-x64", "-c", "Release", "-o", nexusRelayClientPublish], nexusRelayClientProject)

    # Copy Nexus Relay Client.
    shutil.copy(os.path.join(nexusRelayClientPublish, "NexusRelayClient"), finalNexusRelayClientLocation)