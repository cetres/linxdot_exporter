# Linxdot Prometheus Exporter

Exporter for metrics for [Linxdot](https://www.linxdot.com/) miner devices.

The goal of this community-driven initiative is to monitor the Linxdot miner using the open-source [Prometheus platform](https://prometheus.io/). The metrics were discovered by analyzing the responses from the embedded dashboard frontend, as there is currently no official documentation provided by Linxdot.

## Metrics

Metrics identified:

- miner_cpu_temp
- miner_cpu_usage
- miner_mem_usage
- miner_sto_usage

Information:

- animal_name
- firmware version
- model_name
- region
- sn

# Running Local Python Package

A Python package is available for execution of a server of a instance of an exporter providing the follow metrics, an example below:

```
# HELP miner_exporter_info Miner Information
# TYPE miner_exporter_info gauge
miner_exporter_info{animal_name="xxxxxx-xxxxxxx-xxxxxxxx",firmware="Linxdot 1.2.26 r17752-8c4a79dd5",model_name="LD-1001",region="AU915",sn="LD1NTVxxxxxxxxx"} 1.0
# HELP miner_cpu_temp CPU temperature
# TYPE miner_cpu_temp gauge
miner_cpu_temp 35.555
# HELP miner_cpu_usage CPU utilization
# TYPE miner_cpu_usage gauge
miner_cpu_usage 7.169
# HELP miner_mem_usage Memory utilization
# TYPE miner_mem_usage gauge
miner_mem_usage 17.504
# HELP miner_sto_usage Storage utilization
# TYPE miner_sto_usage gauge
miner_sto_usage 39.822
```

Install instructions:

```sh
$ python setup.py install

```

Command line options:

```sh
$ python -m linxdot_exporter --help

usage: __main__.py [-h] [-f LOG_FILE] [-o HOST] [-u USERNAME] [-p PASSWORD] [-a] [-d] [-r REFRESH_INTERVAL] [-t PORT] [--version]

Exporter for metrics for Linxdot miner devices

optional arguments:
  -h, --help            show this help message and exit
  -f LOG_FILE, --log_file LOG_FILE
                        Path of log file
  -o HOST, --host HOST  Miner hostname or IP address
  -u USERNAME, --username USERNAME
                        Miner API username
  -p PASSWORD, --password PASSWORD
                        Miner API password
  -a, --plain_credentials
                        Use login credentials without MD5 hashing
  -d, --debug           Enable debug mode
  -r REFRESH_INTERVAL, --refresh_interval REFRESH_INTERVAL
                        Refresh rate of reading miner API (seconds)
  -t PORT, --port PORT  TCP port number of exporter listens
  --version             show program's version number and exit
```

Execution example:

```sh
$ python -m linxdot_exporter -h miner.hostname -u admin -p xxxxxxxx
```

# Docker

## Standalone

Some variables are required to run at local docker platform:

- MINER_HOST: Miner hostname or IP address
- MINER_USERNAME: Dashboard username
- MINER_PASSWORD: Dashboard password
- EXPORTER_DEBUG: Enable debug mode if setted

Build image:

```sh
$ docker build -t linxdot_exporter .
```

Execute:

```sh
$ docker run --env EXPORTER_DEBUG="True" --env MINER_HOST="xxx.xxx.xxx.xxx" --env MINER_USERNAME="admin" --env MINER_PASSWORD="xxxxxxxx" -p 8061:8061 --name linxdot_exporter linxdot_exporter
```

## Docker Compose

Edit `docker-compose.yml` file and replace variables with miner hostname and credentials. Execute with the following command:

```sh
$ docker-compose up
```


# Third Party Components

This software uses components of the following projects

Prometheus Python client library (https://github.com/prometheus/client_python)

