import sys
import models
import ping
import time
import datetime

def ping_once(session, host):
    latency = None
    error = None
    when = datetime.datetime.now()
    try:
        latency = ping.ping(host)
        print(latency)
    except Exception as e:
        error = str(e)
    
    ping_inst = models.Ping(
        date = when,
        latency = latency,
        error = error,
    )
    session.merge(ping_inst)
    session.commit()

def main(host):
    session = models.open_db(host)
    while True:
        ping_once(session, host)
        time.sleep(10)
    
if __name__ == "__main__":
    google_dns = '8.8.8.8'
    main(google_dns)

    