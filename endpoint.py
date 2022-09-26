import logging as log

from config_settings import EndpointSettings

from ping import ping_endpoint
from suspend import suspend_endpoint
from poweroff import poweroff_endpoint
from wake import wake_endpoint


class Endpoint:
    def __init__(self, name: str, settings: dict) -> None:
        self.name = name
        self.ssh_port = 22
        self.ssh_user = "root"
        self.hostname = None
        self.eth_address = None
        self.enabled = True

        self.parse_config(settings)
        pass

    def pretty_print(self):
        print("Endpoint information")
        print(f"\tName: {self.name}")
        print(f"\tSSH Port: {self.ssh_port}")
        print(f"\tHostname: {self.ssh_user}")
        print(f"\tETH Address: {self.eth_address}")
        print(f"\tEnabled: {self.enabled}")

    def parse_config(self, settings: dict) -> bool:
        for item in settings:
            if item == EndpointSettings.ETH_ADDRESS.value:
                self.eth_address = settings[item]
            elif item == EndpointSettings.HOSTNAME.value:
                self.hostname = settings[item]
            elif item == EndpointSettings.SSH_PORT.value:
                self.ssh_port = settings[item]
            elif item == EndpointSettings.SSH_USER.value:
                self.ssh_user = settings[item]
            elif item == EndpointSettings.ENABLED.value:
                self.enabled = bool(settings[item])

        if not self.hostname:
            log.warning(
                f"Hostname not set for endpoint '{self.name}'. Some features will not be available.")
            return False

        if not self.eth_address:
            log.warning(
                f"Eth Address not set for endpoint '{self.eth_address}'. Some features will not be available.")
            return False

        return True

    def ping(self):
        if not self.enabled:
            return

        if not self.hostname:
            log.warning(f"Ping not available. Hostname is not set.")
            return None

        return ping_endpoint(self.hostname)

    def suspend(self):
        if not self.enabled:
            return

        if not self.hostname:
            log.warning(f"Suspend not available. Hostname is not set.")
            return None

        log.info(
            f"Attempting to suspend '{self.ssh_user}@{self.hostname}:{self.ssh_port}'")
        return suspend_endpoint(hostname=self.hostname, username=self.ssh_user, port=self.ssh_port)

    def poweroff(self):
        if not self.enabled:
            return

        if not self.hostname:
            log.warning(f"Poweroff not available. Hostname is not set.")
            return None

        log.info(
            f"Attempting to poweroff '{self.ssh_user}@{self.hostname}:{self.ssh_port}'")
        return poweroff_endpoint(hostname=self.hostname, username=self.ssh_user, port=self.ssh_port)

    def wake(self):
        if not self.enabled:
            return

        if not self.eth_address:
            log.warning(f"Wake not available. Ethaddr is not set.")
            return None

        log.info(f"Attempting to wake by magic packet '{self.eth_address}'")
        return wake_endpoint(self.eth_address)
