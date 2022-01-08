"""
TheNexusAvenger

Helper script that installs presets.
"""

import sys
from Install import main as installMain
from Util import getOptions


presets = [
    {
        "shortName": "personal-system",
        "name": "Personal System Install",
        "description": "Preset for setting up a personal system (laptop or desktop).",
        "install": ["net6", "wine-tkg", "java", "python3-pip", "vscode", "vim", "roblox", "jetbrains-toolbox", "sqlite-browser", "git", "steam", "minecraft", "nlul", "discord", "chrome", "obs-studio", "openboard", "howdy", "virt-manager",],
    },
    {
        "shortName": "jenkins",
        "name": "Jenkins Install",
        "description": "Preset for setting up a Jenkins server.",
        "install": ["net6", "java", "python3-pip", "vscode", "vim", "sqlite-browser", "git", "virt-manager", "ssh", "vnc", "jenkins", "nexus-relay-client",],
    },
    {
        "shortName": "virtualbox-guest",
        "name": "VirtualBox Guest Install",
        "description": "Preset for setting up an Oracle VirtualBox Guest install. Preparation for Guest Additions included, but installing not included.",
        "install": ["vscode", "python3-pip", "vim", "git", "virtualbox-guest-prepare",],
    },
]


def main():
    """Runs the program.
    """

    # If the first flag is a -y, call the install main function directly.
    # When the install is run with user and root installs, the calling script is re-run with -y in the beginning.
    if len(sys.argv) >= 2 and sys.argv[1].lower() == "-y":
        installMain()
        return

    # Get the install options.
    presetIndices = getOptions(presets)
    installOptions = []
    for presetIndex in presetIndices:
        for option in presets[presetIndex]["install"]:
            if option not in installOptions:
                installOptions.append(option)

    # Run the install.
    installMain(installOptions)


if __name__ == '__main__':
    main()
