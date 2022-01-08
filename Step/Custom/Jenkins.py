"""
TheNexusAvenger

Installs Jenkins and a separate Java version.
"""

import os
import shutil
from Step.Standard.DownloadArchive import downloadArchive
from Step.Standard.DownloadFile import getDownloadLocation
from Step.Standard.RunProcess import runProcess


def installJenkins():
    # Install Jenkins.
    if not os.path.exists("/etc/init.d/jenkins"):
        runProcess(["apt", "install", "-y", "curl"])
        os.system("curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null")
        os.system("echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null")
        runProcess(["apt", "update"])
        try:
            runProcess(["apt", "install", "-y", "jenkins"])
        except Exception:
            # Ignore exceptions that are likely due to the wrong java version being used.
            pass

    # Set up GraalVM.
    # Jenkins requires Java 11, while other programs require newer versions.
    if not os.path.exists("/usr/lib/jvm/java-11-graal"):
        downloadArchive("https://github.com/graalvm/graalvm-ce-builds/releases/download/vm-21.3.0/graalvm-ce-java11-linux-amd64-21.3.0.tar.gz", "tar.gz", "graalvm-11")
        graalDownloadLocation = getDownloadLocation("graalvm-11")
        graalDownloadLocation = os.path.join(graalDownloadLocation, os.listdir(graalDownloadLocation)[0])
        shutil.copytree(graalDownloadLocation, "/usr/lib/jvm/java-11-graal")

    # Add GraalVM to the Jenkins service file path and restart it.
    with open("/etc/init.d/jenkins") as file:
        jenkinsService = file.read()
    if "/usr/lib/jvm/java-11-graal" not in jenkinsService:
        # Modify the file.
        jenkinsService = jenkinsService.replace("PATH=/bin:", "PATH=/usr/lib/jvm/java-11-graal/bin:/bin:")
        with open("/etc/init.d/jenkins", "w") as file:
            file.write(jenkinsService)

        # Restart the service.
        runProcess(["systemctl", "daemon-reload"])
        runProcess(["systemctl", "restart", "jenkins"])