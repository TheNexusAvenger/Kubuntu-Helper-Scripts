"""
TheNexusAvenger

Sets up WINE for Roblox.
"""

import os
import shutil
from Step.Standard.DownloadFile import getDownloadLocation, downloadFile
from Step.Standard.RunProcess import runProcess


def installWine() -> None:
    # Return if WINE already exists.
    finalWinePath = "/usr/local/wine-tkg"
    if os.path.exists(finalWinePath):
        print("WINE already installed to " + finalWinePath)
        return

    # Add the WINE repository.
    wineRepositoryExists = False
    for repositoryFile in os.listdir("/etc/apt/sources.list.d/"):
        if "winehq" in repositoryFile.lower():
            wineRepositoryExists = True
            break
    if not wineRepositoryExists:
        print("Adding WINE repository.")
        downloadFile("https://dl.winehq.org/wine-builds/winehq.key", "winehq.key")
        runProcess(["gpg", "-o", "/etc/apt/trusted.gpg.d/winehq.key.gpg", "--dearmor", getDownloadLocation("winehq.key")])
        runProcess(["apt-add-repository", "https://dl.winehq.org/wine-builds/ubuntu/"])
        runProcess(["apt", "update"])

    # Build wine-tkg.
    wineTkgGitDirectory = getDownloadLocation("wineTkg")
    wineTkgDirectory = os.path.join(wineTkgGitDirectory, "wine-tkg-git")
    wineBuildLocation = os.path.join(wineTkgDirectory, "non-makepkg-builds")
    if not os.path.exists(wineBuildLocation):
        # Enable the source repositories.
        with open("/etc/apt/sources.list", "r") as file:
            sourcesList = file.read()
        if "# deb-src " in sourcesList:
            print("Enabling source repositories.")
            with open("/etc/apt/sources.list", "w") as file:
                file.write(sourcesList.replace("# deb-src ", "deb-src "))
            runProcess(["apt", "update"])

        # Install the wine-tkg build requirements and WINE build requirements.
        print("Installing dependencies.")
        runProcess(["apt", "install", "-y", "git", "autoconf", "flex", "bison"])
        runProcess(["apt", "build-dep", "-y", "wine"])
        runProcess(["apt", "install", "-y", "gcc-multilib", "g++-multilib", "libva-dev", "libpcap-dev", "libgtk-3-dev", "libgstreamer-plugins-base1.0-dev", "libudev-dev", "libkrb5-dev"])

        # Clone the wine-tkg repository.
        if not os.path.exists(wineTkgGitDirectory):
            print("Cloing wine-tkg repository.")
            runProcess(["git", "clone", "--depth=1", "https://github.com/Frogging-Family/wine-tkg-git.git", wineTkgGitDirectory])


        # Modify the customization file.
        print("Preparing configuration.")
        customizationFilePath = os.path.join(wineTkgDirectory, "customization.cfg")
        with open(customizationFilePath) as file:
            customizationFileContents = file.read()
        customizationFileContents = customizationFileContents.replace("_community_patches=\"\"", "_community_patches=\"roblox_mouse_fix.mypatch\"")
        customizationFileContents = customizationFileContents.replace("_nomakepkg_dep_resolution_distro=\"\"", "_nomakepkg_dep_resolution_distro=\"debuntu\"")
        with open(customizationFilePath, "w") as file:
            file.write(customizationFileContents)

        # Enable 32-bit.
        runProcess(["dpkg", "--add-architecture", "i386"])
        runProcess(["apt", "update"])

        # Build wine-tkg.
        print("Building wine-tkg.")
        runProcess(["/bin/bash", "./non-makepkg-build.sh"], wineTkgDirectory)

    # Copy the wine-tkg build files.
    print("Copying wine-tkg files to " + finalWinePath + ".")
    shutil.copytree(os.path.join(wineBuildLocation, os.listdir(wineBuildLocation)[0]), finalWinePath)

    # Create the path file.
    winePathFileLocation = "/etc/profile.d/wine-tkg-path.sh"
    if not os.path.exists(winePathFileLocation):
        with open(winePathFileLocation, "w") as file:
            file.write("export PATH=$PATH:" + os.path.join(finalWinePath, "bin"))
