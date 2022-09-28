import cerberus as cer
import logging as log
import yaml
from enum import Enum


class ConfigKeys(Enum):
    NAME = "name"
    SSH_PORT = "ssh_port"
    HOSTNAME = "hostname"
    SSH_USER = "ssh_username"
    ETH_ADDRESS = "ethaddr"
    ENABLED = "enabled"


ssh_private_key_location = "/ssh/id_rsa"
ssh_known_hosts_location = "/ssh/known_hosts"

schema = {
    'endpoints': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                ConfigKeys.NAME.value: {
                    'required': True,
                    'type': 'string',
                    'minlength': 3,
                    'maxlength': 32
                },
                ConfigKeys.ETH_ADDRESS.value: {
                    'required': True,
                    'type': 'string',
                    'minlength': 17,
                    'maxlength': 17,
                    'regex': '[0-9a-fA-F]{2}([-:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$'
                },
                ConfigKeys.HOSTNAME.value: {
                    'required': True,
                    'type': 'string',
                },
                ConfigKeys.SSH_USER.value: {
                    'required': False,
                    'type': 'string',
                    'default': 'root'
                },
                ConfigKeys.SSH_PORT.value: {
                    'required': False,
                    'type': 'number',
                    'min': 1,
                    'max': 65535,
                    'default': 22
                },
                ConfigKeys.ENABLED.value: {
                    'required': False,
                    'type': 'boolean',
                    'default': True
                }
            }

        },
    }
}


def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            raise exception


def valid_config(config_file):
    doc = load_config(config_file)
    validator = cer.Validator(schema)

    result = validator.validate(doc, schema)

    if not result:
        log.critical(
            f"Invalid configuration file '{config_file}'. Detected problems: {validator.errors}")
        return False

    log.info(f"Config file '{config_file}' seems ok.")
    return True
