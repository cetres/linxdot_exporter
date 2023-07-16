FROM python:3.10-alpine

LABEL MAINTAINER="Gustavo Oliveira <cetres@gmail.com>"
LABEL NAME=linxdot_exporter

WORKDIR /usr/src/app
COPY . .
RUN python setup.py install

EXPOSE 8061/tcp

CMD ["python", "-m" , "linxdot_exporter"]