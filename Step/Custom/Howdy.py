"""
TheNexusAvenger

Sets up Howdy for IR Camera facial recognition.
"""

import os
from Step.Standard.DownloadArchive import downloadArchive
from Step.Standard.DownloadFile import getDownloadLocation
from Step.Standard.RunProcess import runProcess


def installHowdy() -> None:
    # Set up enabling IR emitter.
    if not os.path.exists("/usr/bin/linux-enable-ir-emitter"):
        # Download and install linux-enable-ir-emitter.
        downloadArchive("https://github.com/EmixamPP/linux-enable-ir-emitter/archive/refs/heads/master.zip", "zip", "linux-enable-ir-emitter")
        runProcess(["apt", "install", "-y", "python3-pip"])
        runProcess(["python3", "-m", "pip", "install", "opencv-python"])
        runProcess(["bash", "installer.sh", "install"], os.path.join(getDownloadLocation("linux-enable-ir-emitter"), "linux-enable-ir-emitter-master"))

        # Run the configuration.
        runProcess(["linux-enable-ir-emitter", "configure"])

    # Install Howdy.
    runProcess(["add-apt-repository", "ppa:boltgolt/howdy"])
    runProcess(["apt", "update"])
    runProcess(["apt", "install", "-y", "howdy"])

    # Configure Howdy.
    howdyConfigPath = "/usr/lib/security/howdy/config.ini"
    with open(howdyConfigPath) as file:
        howdyConfig = file.read()
    if "/dev/v4l/by-path/none" in howdyConfig:
        irEmitterConfigPath = "/etc/linux-enable-ir-emitter.yaml"
        device = None
        with open(irEmitterConfigPath) as file:
            for line in file.read().split("\n"):
                if line.strip().startswith("_device"):
                    device = line.split(":")[1].strip()
                    break
        if device is not None:
            howdyConfig = howdyConfig.replace("/dev/v4l/by-path/none", device)
            with open(howdyConfigPath, "w") as file:
                file.write(howdyConfig)
