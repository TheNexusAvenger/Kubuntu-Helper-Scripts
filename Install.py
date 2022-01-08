"""
TheNexusAvenger

Root script for installing programs.
"""

import os.path
import subprocess
import sys
from typing import Dict, List, Optional
from Step.Custom.WineTkg import installWine
from Step.Custom.Grapejuice import installGrapejuice
from Step.Custom.Howdy import installHowdy
from Step.Custom.Jenkins import installJenkins
from Step.Custom.JetBrainsToolbox import installJetBrainsToolbox
from Step.Custom.NexusRelayClient import installNexusRelayClient
from Step.Custom.NexusLULauncher import installNexusLULauncher
from Step.Custom.VNC import installVnc
from Step.Standard.DownloadFile import downloadFileStep, getDownloadLocation
from Step.Standard.RunProcess import runProcessStep
from Step.Standard.InstallApt import installAptStep
from Step.Standard.InstallDebFile import installDebFileStep
from Util import promptConfirm, getOptions


installGroupOrder = ["root", "user"]
installOptions = [
    # SDKs / Runtimes
    {
        "shortName": "net6",
        "name": ".NET 6.0",
        "description": "SDK and Runtime for Microsoft .NET 6. May not work outside Ubuntu versions 21.04 and 21.10.",
        "installAs": "root",
        "install": [
            downloadFileStep("https://packages.microsoft.com/config/ubuntu/21.04/packages-microsoft-prod.deb", "packages-microsoft-prod.deb"),
            installDebFileStep(getDownloadLocation("packages-microsoft-prod.deb")),
            # Microsoft does an update before every install. Not sure why, but this is kept.
            runProcessStep(["apt", "update"]),
            installAptStep(["apt-transport-https"]),
            runProcessStep(["apt", "update"]),
            installAptStep(["dotnet-sdk-6.0"]),
            runProcessStep(["apt", "update"]),
            installAptStep(["aspnetcore-runtime-6.0"]),
        ],
    },
    {
        "shortName": "wine-tkg",
        "name": "WINE for Roblox",
        "description": "WINE build for Roblox.",
        "installAs": "root",
        "install": [
            installWine,
        ],
    },
    {
        "shortName": "java",
        "name": "Oracle JDK",
        "description": "Java Development Kit (JDK) and runtime.",
        "installAs": "root",
        "install": [
            runProcessStep(["add-apt-repository", "ppa:linuxuprising/java"]),
            runProcessStep(["apt", "update"]),
            lambda: subprocess.call(["sudo", "apt", "install", "-y", "oracle-java17-installer", "--install-recommends"])
        ],
    },
    {
        "shortName": "python3-pip",
        "name": "Python 3 Pip",
        "description": "Pip for Python 3",
        "installAs": "root",
        "install": [
            installAptStep(["python3-pip"])
        ],
    },

    # IDEs / Text Editors / Development Tools
    {
        "shortName": "vscode",
        "name": "Microsoft Visual Studio Code",
        "description": "Cross-platform text editor.",
        "installAs": "root",
        "install": [
            downloadFileStep("https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64", "vscode.deb"),
            installDebFileStep(getDownloadLocation("vscode.deb")),
        ],
    },
    {
        "shortName": "vim",
        "name": "VIM",
        "description": "Terminal-based text editor.",
        "installAs": "root",
        "install": [
            installAptStep(["vim"]),
        ],
    },
    {
        "shortName": "roblox",
        "name": "Grapejuice for Roblox",
        "description": "Grapejuice for managing Roblox. Requires roblox-wine to be run first. Can't be run with sudo.",
        "installAs": "user",
        "install": [
            installGrapejuice,
        ],
    },
    {
        "shortName": "jetbrains-toolbox",
        "name": "JetBrains Toolbox",
        "description": "Application for installing and updating JetBrains applications.",
        "installAs": "user",
        "install": [
            installJetBrainsToolbox,
        ],
    },
    {
        "shortName": "sqlite-browser",
        "name": "DB Browser for SQLite",
        "description": "User interface for interacting with SQLite browsers.",
        "installAs": "root",
        "install": [
            installAptStep(["sqlitebrowser"]),
        ],
    },
    {
        "shortName": "git",
        "name": "Git",
        "description": "Distributed source version control tool.",
        "installAs": "root",
        "install": [
            installAptStep(["git"]),
        ],
    },

    # Gaming
    {
        "shortName": "steam",
        "name": "Steam",
        "description": "Steam client for installing games.",
        "installAs": "root",
        "install": [
            installAptStep(["steam-installer"]),
        ],
    },
    {
        "shortName": "minecraft",
        "name": "Minecraft Launcher",
        "description": "Launcher for Minecraft.",
        "installAs": "root",
        "install": [
            downloadFileStep("https://launcher.mojang.com/download/Minecraft.deb", "minecraft.deb"),
            installDebFileStep(getDownloadLocation("minecraft.deb")),
        ],
    },
    {
        "shortName": "nlul",
        "name": "Nexus LU Launcher",
        "description": "Manages setting up LEGO Universe.",
        "installAs": "user",
        "install": [
            installNexusLULauncher,
        ],
    },

    # Communication
    {
        "shortName": "discord",
        "name": "Discord",
        "description": "Cross-platform chat application.",
        "installAs": "root",
        "install": [
            runProcessStep(["add-apt-repository", "ppa:obsproject/obs-studio"]),
            runProcessStep(["apt", "update"]),
            installAptStep(["ffmpeg", "v4l2loopback-dkms", "obs-studio"]),
        ],
    },

    # Other Desktop Applications
    {
        "shortName": "chrome",
        "name": "Google Chrome",
        "description": "Web browser with profile synchronization.",
        "installAs": "root",
        "install": [
            downloadFileStep("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "chrome.deb"),
            installDebFileStep(getDownloadLocation("chrome.deb")),
        ],
    },
    {
        "shortName": "obs-studio",
        "name": "Open Broadcaster Software Studio",
        "description": "Cross-platform recording and streaming tool.",
        "installAs": "root",
        "install": [
            downloadFileStep("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "chrome.deb"),
            installDebFileStep(getDownloadLocation("chrome.deb")),
        ],
    },
    {
        "shortName": "openboard",
        "name": "OpenBoard",
        "description": "Whiteboard application for active pens.",
        "installAs": "root",
        "install": [
            installAptStep(["openboard"]),
        ],
    },

    # Desktop Utilities
    {
        "shortName": "howdy",
        "name": "Howdy",
        "description": "Enables authentication with IR cameras similar to Windows Hello.",
        "installAs": "root",
        "install": [
            installHowdy,
        ],
    },

    # Virtualization
    {
        "shortName": "virtualbox-guest-prepare",
        "name": "VirtualBox Guest Additions Build Tools",
        "description": "Build tools required for setting up VirtualBox Guest Additions.",
        "installAs": "root",
        "install": [
            installAptStep(["build-essential", "dkms"]),
        ],
    },
    {
        "shortName": "virt-manager",
        "name": "Virtual Machine Manager",
        "description": "Graphical user interface for virtual machines. Includes virtualization tools like QEMU.",
        "installAs": "root",
        "install": [
            installAptStep(["virt-manager"]),
        ],
    },

    # Server Applications
    {
        "shortName": "ssh",
        "name": "SSH Server",
        "description": "Server connecting over SSH.",
        "installAs": "root",
        "install": [
            installAptStep(["openssh-server"]),
        ],
    },
    {
        "shortName": "vnc",
        "name": "VNC Server",
        "description": "Server for connecting with a graphical display.",
        "installAs": "root",
        "install": [
            installVnc,
        ],
    },
    {
        "shortName": "jenkins",
        "name": "Jenkins",
        "description": "Server for running automation jobs.",
        "installAs": "root",
        "install": [
            installJenkins,
        ],
    },
    {
        "shortName": "nexus-relay-client",
        "name": "Nexus Relay Client",
        "description": "Client for forwarding traffic with Nexus Relay.",
        "installAs": "root",
        "install": [
            installNexusRelayClient,
        ],
    },
]


def getInstallOptions(arguments: Optional[List] = None) -> (List[int], bool):
    """Gets the options to install.

    :param: arguments Optional overrides for the command line.
    :return: Set of index options to install.
    """

    # Remove the confirm flag if one exists.
    if arguments is None:
        arguments = sys.argv[1:]
    autoConfirm = False
    if "-y" in arguments:
        arguments.remove("-y")
        autoConfirm = True

    # Return the valid arguments.
    return getOptions(installOptions, arguments), autoConfirm


def install(installData: Dict) -> None:
    """Installs an application.

    :param installData: Data about the app from installOptions.
    """

    print("Installing " + installData["name"])
    for step in installData["install"]:
        step()
    print("Installed " + installData["name"])


def main(arguments: Optional[List] = None) -> None:
    """Runs the program.
    """

    # Get the options to install.
    selectedInstallOptionIndexes, autoConfirm = getInstallOptions(arguments)
    if len(installOptions) == 0:
        print("No options were specified.")
        exit(-1)

    # Prompt to install.
    shortNames = []
    for i in range(0, len(selectedInstallOptionIndexes)):
        shortNames.append(installOptions[selectedInstallOptionIndexes[i]]["shortName"])
    if not autoConfirm and not promptConfirm("Confirm installing " + ", ".join(shortNames) + "?"):
        exit(1)

    # Group the applications to install.
    groupedShortNames = {}
    for i in range(0, len(selectedInstallOptionIndexes)):
        installData = installOptions[selectedInstallOptionIndexes[i]]
        installAs = installData["installAs"].lower()
        if installAs not in groupedShortNames.keys():
            groupedShortNames[installAs] = []
        groupedShortNames[installAs].append(installData["shortName"])

    # Move the any groupings to root then user.
    if "any" in groupedShortNames.keys():
        if "root" in groupedShortNames.keys():
            groupedShortNames["root"].extend(groupedShortNames["any"])
        elif "user" in groupedShortNames.keys():
            groupedShortNames["user"].extend(groupedShortNames["any"])
        else:
            groupedShortNames["root"] = groupedShortNames["any"]
        groupedShortNames.pop("any")

    # Ensure root access.
    isRoot = os.path.expanduser("~").startswith("/root")
    if "user" in groupedShortNames.keys() and isRoot:
        print("Some selected options must be installed as the user. Do not use root.")
        exit(-1)

    if len(groupedShortNames.keys()) >= 2 or (not isRoot and "root" in groupedShortNames.keys()):
        # Call the original script with the options.
        for group in installGroupOrder:
            if group in groupedShortNames.keys():
                # Build the arguments.
                arguments = []
                if group == "root":
                    arguments.append("sudo")
                arguments.extend([sys.executable, sys.argv[0], "-y"])
                arguments.extend(groupedShortNames[group])

                # Run the process.
                scriptExitCode = subprocess.call(arguments, cwd=os.getcwd())
                if scriptExitCode != 0:
                    exit(scriptExitCode)
    else:
        # Install the options.
        for i in range(0, len(selectedInstallOptionIndexes)):
            installData = installOptions[selectedInstallOptionIndexes[i]]
            try:
                install(installData)
            except Exception as e:
                print(e)
                baseErrorMessage = "Error occurred when installing " + installData["name"] + "."
                if i == len(selectedInstallOptionIndexes) - 1:
                    print(baseErrorMessage)
                    exit(-1)
                else:
                    if not promptConfirm(baseErrorMessage + " Continue?"):
                        exit(-1)


if __name__ == '__main__':
    main()
