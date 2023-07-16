
import logging
import time
from typing import Dict
from urllib.parse import urljoin

from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily

import requests

from .exceptions import LoginFailedException, RequestException

class LinxdotCollector(object):
    _base_url = str
    _login_params: Dict[str, str]
    _sess: requests.Session = None
    _refresh_interval = None
    _collection_validity = 0
    _last_collection = None

    def __init__(self, host: str, username: str, password: str, refresh_interval=None, secure=False) -> None:
        self._base_url = f'http{"s" if secure else ""}://{host}/'
        self._login_params = {
            'username': username,
            'password': password
        }
        self._refresh_interval = refresh_interval
    
    @property
    def sess(self):
        if self._sess is None:
            logging.debug('Starting a new session...')
            self._sess = requests.session()
            self.login()
        return self._sess

    def login(self) -> None:
        url = urljoin(self._base_url, 'login_odd')
        logging.debug(f'Login at url {url} with username {self._login_params["username"]}')
        r = self.sess.post(url, data=self._login_params)
        if r.status_code != 200:
            logging.warn(f'Login failed at {url} - HTTP error code: {r.status_code}')
            raise LoginFailedException()
    
    def info(self) -> Dict[str, str]:
        ts = int(time.time())
        if self._refresh_interval is None or self._collection_validity < ts:
            url = urljoin(self._base_url, 'info/system')
            r = self.sess.get(url)
            if r.status_code != 200:
                logging.warn(f'Status failed at {url} - HTTP error code: {r.status_code}')
                raise RequestException()
            self._last_collection = r.json()
            if self._refresh_interval is not None:
                self._collection_validity = ts + self._refresh_interval
        else:
            logging.debug('Cache hit')
        return self._last_collection

    def collect(self):
        logging.debug('Running collector')
        info = self.info()
        logging.debug(f'Info: {info}')

        info_metric = InfoMetricFamily("miner_exporter", "Miner Information",
                                       labels=[])
        info_metric.add_metric([], {
            'animal_name': info['animal_name'],
            'region': info['region'],
            'firmware': info['firmware'],
            'model_name': info['model_name'],
            'sn': info['sn'],
        })
        yield info_metric

        gauge_cpu_temp = GaugeMetricFamily("miner_cpu_temp", "CPU temperature")
        gauge_cpu_temp.add_metric([], info["cpu_temp"])
        yield gauge_cpu_temp

        gauge_cpu_usage = GaugeMetricFamily("miner_cpu_usage", "CPU utilization")
        gauge_cpu_usage.add_metric([], round(info["cpu_usage"], 3))
        yield gauge_cpu_usage

        gauge_mem_usage = GaugeMetricFamily("miner_mem_usage", "Memory utilization")
        gauge_mem_usage.add_metric([], round(info["memory_usage"], 3))
        yield gauge_mem_usage

        gauge_sto_usage = GaugeMetricFamily("miner_sto_usage", "Storage utilization")
        gauge_sto_usage.add_metric([], round(info["storage_usage"], 3))
        yield gauge_sto_usage