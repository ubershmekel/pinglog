import sys
import models
import ping
import time
import datetime
import traceback
import csv
import os

def ping_once(session, host):
    latency = None
    error = None
    when = datetime.datetime.now()
    try:
        latency = ping.ping(host)
        print(latency)
    except Exception as e:
        error = str(e)
        traceback.print_exc()
    
    ping_inst = models.Ping(
        date = when,
        latency = latency,
        error = error,
    )
    session.merge(ping_inst)
    session.commit()

def ping_loop(hosts):
    while True:
        for host in hosts:
            session = models.open_db(host)
            ping_once(session, host)
        time.sleep(10)

def get_hosts():
    ping_hosts_file = 'hosts.csv'
    if os.path.exists(ping_hosts_file):
        reader = csv.DictReader(open(ping_hosts_file))
        hosts = [row['host'] for row in reader]
        return hosts
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
    
