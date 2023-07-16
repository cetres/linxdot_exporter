import argparse
import hashlib
import logging
import os
import time
import sys

from prometheus_client import REGISTRY, start_http_server, Summary

from .collector import LinxdotCollector
from .constants import DEFAULT_REFRESH_INTERVAL, DEFAULT_EXPORTER_PORT
from .version import __version__

def hash_cred(text):
    return hashlib.md5(text.encode()).hexdigest()

def run_server(args):
    logging.basicConfig(filename=args.log_file, format='%(levelname)s: %(message)s',
                    level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting server. Version {__version__}')
    username = args.username if args.plain_credentials else hash_cred(args.username)
    password = args.password if args.plain_credentials else hash_cred(args.password)

    collector = LinxdotCollector(args.host, username, password, args.refresh_interval)
    REGISTRY.register(collector)

    start_http_server(args.port)
    
    while True:
        time.sleep(args.refresh_interval)


def exec_cmd():
    parser = argparse.ArgumentParser(description='''Exporter for metrics for Linxdot miner devices''')
    parser.add_argument('-f', '--log_file', default=os.environ.get('LOG_FILE'), 
                        help='Path of log file')
    parser.add_argument('-o', '--host', default=os.environ.get('MINER_HOST'), 
                        help='Miner hostname or IP address')
    parser.add_argument('-u', '--username', default=os.environ.get('MINER_USERNAME'), 
                        help='Miner API username')
    parser.add_argument('-p', '--password', default=os.environ.get('MINER_PASSWORD'), 
                        help='Miner API password')
    parser.add_argument('-a', '--plain_credentials', action='store_true',
                        default=os.environ.get('PLAIN_CREDENTIALS', False),
                        help='Use login credentials without MD5 hashing')
    parser.add_argument('-d', '--debug', action='store_true',
                        default=os.environ.get('EXPORTER_DEBUG', False),
                        help='Enable debug mode')
    parser.add_argument('-r', '--refresh_interval', type=int,
                        default=os.environ.get('EXPORTER_REFRESH', DEFAULT_REFRESH_INTERVAL), 
                        help='Refresh rate of reading miner API (seconds)')
    parser.add_argument('-t', '--port', type=int,
                        default=os.environ.get('EXPORTER_PORT', DEFAULT_EXPORTER_PORT), 
                        help='TCP port number of exporter listens')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    if args.host is None or args.username is None or args.password is None:
        print("Required arguments or environment variables: HOST, USERNAME and PASSWORD")
        sys.exit(1)
    run_server(args)
