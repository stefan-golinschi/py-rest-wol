from enum import Enum


class EndpointSettings(Enum):
    NAME = "name"
    SSH_PORT = "ssh_port"
    HOSTNAME = "hostname"
    SSH_USER = "ssh_username"
    ETH_ADDRESS = "ethaddr"
    ENABLED = "enabled"
