#! python3

import matplotlib.pyplot as plt

import models
import main



def chart(pings):
    xs = []
    ys = []
    red_xs = []
    red_ys = []
    for ping in pings:
        if ping.latency is not None:
            xs.append(ping.date)
            ys.append(ping.latency)
        if ping.error is not None:
            red_xs.append(ping.date)
            red_ys.append(1000)
        
    print(min(xs))
    print(max(xs))
    plt.xlim((min(xs), max(xs)))
    plt.scatter(xs, ys, alpha=0.1)
    plt.scatter(red_xs, red_ys, c='r', s=100)

for host in main.get_hosts():    
    session = models.open_db(host)
    chart(session.query(models.Ping))

plt.show()

