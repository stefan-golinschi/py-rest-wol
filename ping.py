import subprocess
from sys import stdout
import logging as log

# default options
ping_count = 1
ping_timeout = 3

def ping_endpoint(hostname: str):
    response = subprocess.run(
        ["ping", "-c", str(ping_count), "-W", str(ping_timeout), hostname],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return response.returncode

