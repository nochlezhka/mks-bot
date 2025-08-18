FROM python:3.13.7-alpine

#
# Create a base UID/GID and SUID/SGID which will be used by container
#
RUN addgroup -S --gid 1000 tbot \
 && adduser -S -G tbot -u 1000 -s /bin/bash tbot \
 && mkdir -p /run/user/1000 \
 && chown -R tbot /run/user/1000 /home/tbot \
 && echo tbot:100000:65536 | tee /etc/subuid | tee /etc/subgid

ENV HOME=/home/tbot \
    USER=tbot \
    XDG_RUNTIME_DIR=/run/user/1000

RUN mkdir -p ${HOME}/bot

RUN apk update \
 && apk add --virtual python3-dev musl-dev libpng-dev build-base gcc freetype-dev pkgconfig

COPY requirements.txt ${HOME}/bot

RUN pip3 install --upgrade pip \
 && pip3 install --no-cache-dir --prefer-binary -r ${HOME}/bot/requirements.txt

USER tbot
COPY ./src ${HOME}/bot/src
COPY ./resources ${HOME}/bot/resources

WORKDIR ${HOME}/bot/src
ENTRYPOINT ["python3", "main.py"]
