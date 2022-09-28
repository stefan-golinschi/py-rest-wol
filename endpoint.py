import logging as log

from config import ConfigKeys
from ping import ping_endpoint
from suspend import suspend_endpoint
from poweroff import poweroff_endpoint
from wake import wake_endpoint


class Endpoint:
    def __init__(self, settings: dict) -> None:
        self.name = None
        self.ssh_port = 22
        self.ssh_user = "root"
        self.hostname = None
        self.eth_address = None
        self.enabled = True

        self.configure(settings)

    def pretty_print(self):
        print("Endpoint information")
        print(f"\tName: {self.name}")
        print(f"\tSSH Port: {self.ssh_port}")
        print(f"\tHostname: {self.ssh_user}")
        print(f"\tETH Address: {self.eth_address}")
        print(f"\tEnabled: {self.enabled}")

    def configure(self, settings: dict):
        for item in settings:
            if item == ConfigKeys.NAME.value:
                self.name = settings[item]
            if item == ConfigKeys.ETH_ADDRESS.value:
                self.eth_address = settings[item]
            elif item == ConfigKeys.HOSTNAME.value:
                self.hostname = settings[item]
            elif item == ConfigKeys.SSH_USER.value:
                self.ssh_user = settings[item]
            elif item == ConfigKeys.SSH_PORT.value:
                self.ssh_port = settings[item]
            elif item == ConfigKeys.ENABLED.value:
                self.enabled = bool(settings[item])

        if not self.enabled:
            log.warning(f"'{self.name}' is configured as disabled.")

    def ping(self):
        if not self.enabled:
            return

        log.info(
            f"Trying to ping '{self.name}', '{self.ssh_user}@{self.hostname}:{self.ssh_port}'")
        return ping_endpoint(self.hostname)

    def suspend(self):
        if not self.enabled:
            return

        log.info(
            f"Trying to suspend '{self.name}', '{self.ssh_user}@{self.hostname}:{self.ssh_port}'")
        return suspend_endpoint(hostname=self.hostname, username=self.ssh_user, port=self.ssh_port)

    def poweroff(self):
        if not self.enabled:
            return

        log.info(
            f"Trying to poweroff '{self.name}', '{self.ssh_user}@{self.hostname}:{self.ssh_port}'")
        return poweroff_endpoint(hostname=self.hostname, username=self.ssh_user, port=self.ssh_port)

    def wake(self):
        if not self.enabled:
            return

        log.info(
            f"Trying to wake '{self.name}', ethaddr: {self.eth_address}")
        return wake_endpoint(self.eth_address)
