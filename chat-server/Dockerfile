ARG APP_PATH="/usr/local/chat-server"

######################################################
# build
######################################################
FROM python:3.11-slim as build

RUN apt-get update && apt-get install -y build-essential

ARG APP_PATH
WORKDIR "${APP_PATH}"

RUN python -m venv "${APP_PATH}/venv"
ENV PATH="${APP_PATH}/venv/bin:$PATH"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt --no-cache-dir

######################################################
# deploy
######################################################
FROM python:3.11-slim

ARG APP_PATH
WORKDIR "${APP_PATH}"

RUN groupadd python && useradd -g python -s /bin/sh -M python
USER python

COPY --from=build --chown=python:python ["${APP_PATH}", "."]
COPY --chown=python:python ./app ./app

ENV PATH="${APP_PATH}/venv/bin:$PATH"

ENV SERVER_PORT="80"
EXPOSE 80/tcp
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "app.main:get_default_app()"]
