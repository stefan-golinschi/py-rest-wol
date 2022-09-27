import cerberus as cer
import logging as log
import yaml


schema = {
    'endpoints': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'required': True,
                    'type': 'string',
                    'minlength': 3,
                    'maxlength': 32
                },
                'ethaddr': {
                    'required': True,
                    'type': 'string',
                    'minlength': 17,
                    'maxlength': 17,
                    'regex': '[0-9a-fA-F]{2}([-:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$'
                },
                'hostname': {
                    'required': True,
                    'type': 'string',
                },
                'ssh_username': {
                    'required': False,
                    'type': 'string',
                    'default': 'root'
                },
                'ssh_username': {
                    'required': False,
                    'type': 'string',
                    'default': 'root'
                },
                'ssh_port': {
                    'required': False,
                    'type': 'number',
                    'min': 1,
                    'max': 65535,
                    'default': 22
                },
                'enabled': {
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
