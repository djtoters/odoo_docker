FROM python:3.10-slim-bookworm AS builder
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl cups libcups2-dev gcc zlib1g-dev node-less libxslt1-dev libxml2-dev python-dev-is-python3 libfreetype6-dev libsasl2-dev libldap2-dev libssl-dev libjpeg-dev zlib1g-dev python3-lxml libtool make python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++

COPY ./requirements.txt .
RUN python3 -m pip install --target=/root/python -r requirements.txt

FROM python:3.10-slim-bookworm AS runner
COPY --from=builder /root /root

RUN apt-get update && apt-get install -y node-less xmlsec1 curl
ENV PYTHONPATH=/root/python

WORKDIR /opt/odoo