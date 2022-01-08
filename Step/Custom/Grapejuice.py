"""
TheNexusAvenger

Sets up Grapejuice.
"""

import os
import subprocess
from Step.Standard.DownloadFile import getDownloadLocation
from Step.Standard.RunProcess import runProcess


def installGrapejuice() -> None:
    # Throw an exception if WINE is not installed.
    if not os.path.exists("/usr/local/wine-tkg"):
        raise Exception("WINE for Roblox not found. Install roblox-wine first.")

    # Return if Grapejuice already exists.
    grapejuiceInstallPath = os.path.expanduser("~/.local/bin/grapejuice")
    if os.path.exists(grapejuiceInstallPath):
        print("Grapejuice already installed.")
        return

    # Install the dependencies.
    runProcess(["sudo", "apt", "install", "-y", "git", "python3-pip", "python3-setuptools", "python3-wheel", "python3-dev", "pkg-config", "mesa-utils", "libcairo2-dev", "gtk-update-icon-cache", "desktop-file-utils", "xdg-utils", "libgirepository1.0-dev", "gir1.2-gtk-3.0", "gnutls-bin:i386"])

    # Clone the Grapejuice repository.
    grapejuiceGitDirectory = getDownloadLocation("Grapejuice")
    if not os.path.exists(grapejuiceGitDirectory):
        print("Cloing Grapejuice repository.")
        runProcess(["git", "clone", "https://gitlab.com/brinkervii/grapejuice.git", grapejuiceGitDirectory])

    # Run the setup.
    environment = os.environ.copy()
    environment["PATH"] = environment["PATH"] + ":/usr/local/wine-tkg/bin"
    process = subprocess.Popen(["python3", "./install.py"], cwd=grapejuiceGitDirectory, env=environment)
    process.wait()
    if process.returncode != 0:
        raise Exception("Process returned an error code " + str(process.returncode))
