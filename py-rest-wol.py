import logging as log
import argparse
import yaml
import os

from endpoint import Endpoint
from config import valid_config, load_config


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


def main():
    create_logger()

    args = argument_parser()
    config_file = args.config

    if not valid_config(config_file):
        exit(1)

    config = load_config(config_file)['endpoints']

    endpoints = []

    for item in config:
        settings = item

        ep = Endpoint(settings)
        endpoints.append(ep)

        print(f"{ep.name}: {ep.ping()}")


if __name__ == "__main__":
    main()
