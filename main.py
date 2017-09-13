"""
Ping 
"""

import sys
import models
import ping
import time
import datetime
import traceback
import json
import os

SECONDS_BETWEEN_PINGS = 10
DEFAULT_DB_FILE = 'pingsdb.sqlite'

def ping_once(session, host):
    latency = None
    error = None
    when = datetime.datetime.now()
    try:
        latency = ping.ping(host)
    except Exception as e:
        error = str(e)
        traceback.print_exc()
    
    ping_inst = models.Ping(
        date = when,
        host = host,
        latency = latency,
        error = error,
    )
    session.merge(ping_inst)
    session.commit()
    print(ping_inst)

def ping_loop(hosts, db_file=DEFAULT_DB_FILE):
    session = models.open_db(db_file)
    while True:
        for host in hosts:
            ping_once(session, host)
        time.sleep(SECONDS_BETWEEN_PINGS)

def get_hosts():
    """
    Example configuration file:
        {
            "hosts": ["8.8.8.8"]
        }
    """
    ping_config_file = 'config.json'
    if os.path.exists(ping_config_file):
        print('Loading config from %s' % ping_config_file)
        config = json.load(open(ping_config_file))
        if 'hosts' in config:
            return config['hosts']
    else:
        return []

def main():
    hosts = get_hosts()
    if not hosts:
        google_dns = '8.8.8.8'
        hosts = [google_dns]
    ping_loop(hosts)

if __name__ == "__main__":
    main()
    
