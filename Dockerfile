FROM python:3-alpine

LABEL org.opencontainers.image.authors="stefan.golinschi@gmail.com"
LABEL org.opencontainers.image.source="https://github.com/stefan-golinschi/py-rest-wol.git"

ENV LOG_LEVEL="debug"

RUN mkdir /app
COPY ${PWD}/requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY \
    ${PWD}/config.py \
    ${PWD}/endpoint.py \
    ${PWD}/ping.py \
    ${PWD}/poweroff.py \
    ${PWD}/py-rest-wol.py \
    ${PWD}/suspend.py \
    ${PWD}/wake.py \
    ${PWD}/remotecmd.py \
    /app/

ENTRYPOINT [ "/usr/local/bin/python3",  "/app/py-rest-wol.py" ]
