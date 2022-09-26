import logging as log
import argparse
import yaml
import ping


def create_logger():
    FORMAT = "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(funcName)s() %(message)s"
    log.basicConfig(format=FORMAT, level=log.DEBUG)

def argument_parser():
    parser = argparse.ArgumentParser(description="Restful application that provides WOL/suspend/ping services.")
    parser.add_argument("-c", "--config", type=str, help="path to the config file")

    return parser.parse_args()

def valid_config(config_file:str) -> bool:
    import os.path

    if not os.path.exists(config_file):
        log.critical(f"Config file does not exist '{config_file}'.")
        return False

    log.info(f"Using config file '{config_file}'.")
    return True

from endpoint import Endpoint

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

    for item in config["endpoints"]:
        endpoint_name = item
        settings = config["endpoints"][endpoint_name]
        
        ep = Endpoint(endpoint_name, settings)
        ep.pretty_print()
        if ep.name == "homeserver":
            ep.wake()

if __name__ == "__main__":
    main()