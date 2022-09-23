import logging as log

FORMAT = '[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(funcName)s() %(message)s'
log.basicConfig(format=FORMAT, level=log.DEBUG)

import ping

hosts = [
    "127.0.0.1",
    "homeserver.lan",
    "not_existent.lan",
    "xsvm.eu",
    "facebook.com",
    "homerouter.lan"
]

for host in hosts:
    ret = ping.ping_endpoint(host)
    log.info(f"{host}: {ret}")
