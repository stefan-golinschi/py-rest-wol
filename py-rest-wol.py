import logging as log
import argparse
from fastapi import FastAPI
import uvicorn
import os

from endpoint import Endpoint
from config import valid_config, load_config


class MainApp:
    def __init__(self, log_level: str = "info") -> None:
        self.log_level = log_level

        self.__configure_logger()
        self.__configure_argument_parser()
        self.__load_config()

    def __configure_logger(self):
        if not self.log_level:
            self.log_level = "info"

        if self.log_level == "info":
            level = log.INFO
        elif self.log_level == "debug":
            level = log.DEBUG
        elif self.log_level == "warning":
            level = log.WARNING

        FORMAT = "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(funcName)s() %(message)s"
        log.basicConfig(format=FORMAT, level=level)

        log.info(f"Log level has been set to '{self.log_level}'")

    def __configure_argument_parser(self):
        parser = argparse.ArgumentParser(
            description="Restful application that provides WOL/suspend/ping services.")
        parser.add_argument("-c", "--config", type=str, required=True,
                            help="path to the config file")

        self.args = parser.parse_args()

    def __load_config(self):
        config_file = self.args.config

        if not valid_config(config_file):
            exit(1)

        configs = load_config(config_file)
        configs = configs['endpoints']

        self.endpoints: dict[Endpoint] = {}

        for item in configs:
            ep = Endpoint(item)
            self.endpoints[ep.name] = ep

    def get_endpoint_by_name(self, name: str):
        if name in self.endpoints:
            return self.endpoints[name]

        return None


class RestResponse:
    def __init__(self, method: str, status: int = None, message: str = None) -> None:
        self.method = method
        self.status = status
        self.msg = message

    def create(self):
        return {
            "method": self.method,
            "status": self.status,
            "message": self.msg
        }


log_level = os.getenv("LOG_LEVEL")
listen_port = os.getenv("LISTEN_PORT")
listen_address = os.getenv("LISTEN_ADDRESS")

app = FastAPI()
application = MainApp(log_level)

if __name__ == "__main__":
    if not listen_address:
        listen_address = "0.0.0.0"
        log.info(f"Using default listening address: {listen_address}")

    if not listen_port:
        listen_port = 8091
        log.info(f"Using default listening port: {listen_port}")

    uvicorn.run("py-rest-wol:app", host=listen_address,
                port=int(listen_port), log_level="info")


@ app.on_event("startup")
async def startup_event():
    log_level = os.getenv('LOG_LEVEL')
    application = MainApp(log_level)


@ app.get("/ping/{endpoint_name}")
async def ping(endpoint_name):
    ep = application.get_endpoint_by_name(endpoint_name)

    response = RestResponse(ping.__name__)
    if not ep:
        response.msg = "Endpoint not found"
        return response.create()

    status = ep.ping()
    response.status = status
    if status == None:
        response.msg = "disabled"
    elif status == True:
        response.msg = "up"
    elif status == False:
        response.msg = "down"

    return response.create()


@ app.get("/suspend/{endpoint_name}")
async def suspend(endpoint_name):
    ep = application.get_endpoint_by_name(endpoint_name)
    response = RestResponse(suspend.__name__)

    if not ep:
        response.msg = "Endpoint not found"
        return response.create()

    response.status = ep.suspend()
    if response.status:
        response.msg = "Sent suspend command"
    else:
        response.msg = "Cannot suspend."

    return response.create()


@ app.get("/poweroff/{endpoint_name}")
async def poweroff(endpoint_name):
    ep = application.get_endpoint_by_name(endpoint_name)
    response = RestResponse(poweroff.__name__)

    if not ep:
        response.msg = "Endpoint not found"
        return response.create()

    response.status = ep.suspend()
    if response.status:
        response.msg = "Sent poweroff command"
    else:
        response.msg = "Cannot suspend."

    return response.create()


@ app.get("/wake/{endpoint_name}")
async def wake(endpoint_name):
    ep = application.get_endpoint_by_name(endpoint_name)
    response = RestResponse(wake.__name__)

    if not ep:
        response.msg = "Endpoint not found"
        return response.create()

    response.status = ep.wake()
    response.msg = "Tried to wake."
    return response.create()
