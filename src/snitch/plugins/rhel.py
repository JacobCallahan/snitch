"""Provides a Snitch plugin for RHEL-based systems."""

from pathlib import Path
import subprocess

from snitch.decorators import check
from snitch.logging import logger


class RHEL:
    """A plugin for checking activity on RHEL-based systems."""

    name = "RHEL"
    files = [
        {"path": "/var/log/secure", "weight": 3},
        {"path": "/var/log/messages", "weight": 1},
        {"path": "/var/log/cron", "weight": 2},
        {"path": "/var/log/audit/audit.log", "weight": 2},
        {"path": "/var/log/lastlog", "weight": 3},
        {"path": "/etc/passwd", "weight": 1},
    ]

    @staticmethod
    def is_applicable():
        """Check if this plugin is applicable to the current system."""
        return Path("/etc/redhat-release").exists()

    @check(weight=3)
    def logged_in_users(self):
        """Check for currently logged-in users.

        Returns True if one or more users are found to be 'still logged in'.
        """
        try:
            res = subprocess.run(["last", "-n", "20"], capture_output=True, text=True, check=False)
            for line in res.stdout.splitlines():
                if "still logged in" in line:
                    return True
            return False
        except (FileNotFoundError, subprocess.SubprocessError) as e:
            logger.error(f"      -> Could not execute 'last' command: {e}")
            return False
