import logging as log
import argparse
import yaml
import os

from endpoint import Endpoint


def create_logger():
    log_level = os.getenv('LOG_LEVEL')

    # default level will be info
    level = log.INFO

    if log_level == "info":
        level = log.INFO
    elif log_level == "debug":
        level = log.DEBUG
    elif log_level == "warning":
        level = log.WARNING

    FORMAT = "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(funcName)s() %(message)s"
    log.basicConfig(format=FORMAT, level=level)


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Restful application that provides WOL/suspend/ping services.")
    parser.add_argument("-c", "--config", type=str, required=True,
                        help="path to the config file")

    return parser.parse_args()


def valid_config(config_file: str) -> bool:
    import os.path

    if not os.path.exists(config_file):
        log.critical(f"Config file does not exist '{config_file}'.")
        return False

    log.info(f"Using config file '{config_file}'.")
    return True


def main():
    create_logger()

    args = argument_parser()
    config_file = args.config

    if not valid_config(config_file):
        exit(1)

    with open(config_file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            log.critical(e)

    endpoints = []
    for item in config["endpoints"]:
        endpoint_name = item
        settings = config["endpoints"][endpoint_name]

        ep = Endpoint(endpoint_name, settings)
        endpoints.append(ep)

    print(endpoints[0].suspend())


if __name__ == "__main__":
    main()
