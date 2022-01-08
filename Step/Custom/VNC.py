"""
TheNexusAvenger

Installs a VNC server.
"""

import os
from Step.Standard.RunProcess import runProcess


def installVnc() -> None:
    # Install X11 VNC.
    runProcess(["apt", "install", "-y", "x11vnc"])

    # Create the password file.
    if not os.path.exists("/etc/x11vnc.passwd"):
        runProcess(["x11vnc", "-storepasswd", "/etc/x11vnc.passwd"])
        runProcess(["chmod", "0400", "/etc/x11vnc.passwd"])

    # Create and start the service.
    if not os.path.exists("/etc/systemd/system/x11vnc.service"):
        # Write the service file.
        with open("/etc/systemd/system/x11vnc.service", "w") as file:
            file.write("[Unit]\r\n")
            file.write("Description=Start x11vnc\r\n")
            file.write("After=multi-user.target display-manager.service\r\n")
            file.write("\r\n")
            file.write("[Service]\r\n")
            file.write("Type=simple\r\n")
            file.write("ExecStart=/bin/sh -c '/usr/bin/x11vnc -display :0 -forever  -rfbport 5900 -xkb -noxrecord -noxfixes -noxdamage -nomodtweak -repeat -shared -norc -auth /var/run/sddm/* -rfbauth /etc/x11vnc.passwd'\r\n")
            file.write("Restart=always\r\n")
            file.write("RestartSec=1\r\n")
            file.write("ExecStop=/usr/bin/killall x11vnc\r\n")
            file.write("\r\n")
            file.write("[Install]\r\n")
            file.write("WantedBy=multi-user.target")

        # Start the service.
        runProcess(["systemctl", "daemon-reload"])
        runProcess(["systemctl", "start", "x11vnc"])
        runProcess(["systemctl", "enable", "x11vnc"])