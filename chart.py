#! python3

import glob
import datetime
import itertools

import matplotlib.pyplot as plt
import numpy as np

import models

PING_FOR_ERRORS = 500

def chart(pings):
    type_x_y = []
    for ping in pings:
        if ping.latency is not None:
            type_x_y.append([ping.host, ping.date, ping.latency])
        if ping.error is not None:
            if '8.8.8.8' in ping.host:
                fake_latency = 900
            else:
                fake_latency = 700
            type_x_y.append([ping.host + '-error', ping.date, fake_latency])
    
    type_x_y = sorted(type_x_y)
    prev = None
    for a, b, c in type_x_y:
        if prev != a:
            print(a)
            prev = a
    
    type_x_y = np.array(type_x_y)
    min_x = min(type_x_y[:, 1])
    max_x = max(type_x_y[:, 1])
    #print(min(xs))
    #print(max(xs))
    #plt.xlim((min(xs), max(xs)))
    #plt.ylim((0, max(ys + red_ys)))
    def first(seq):
        return seq[0]

    for key, group in itertools.groupby(type_x_y, key=first):
        xs = []
        ys = []
        for _host, dt, latency in group:
            xs.append(dt)
            ys.append(latency)
        #group.shape = ()
        #print(group.shape)
        #print(list(group))
        print('%s %s' % (repr(key), len(ys)))
        #xs, ys = group[:, 1], group[:, 2]
        alpha = 0.2
        if 'error' in key:
            alpha = 0.8
        plt.scatter(xs, ys, alpha=alpha, label=key)
    #plt.scatter(red_xs, red_ys, c='r', s=100, label="errors")
    plt.xlim((min_x, max_x))
    plt.legend()

since = datetime.datetime.now() - datetime.timedelta(days=14)

for db_file in glob.glob('*.sqlite'):
    session = models.open_db(db_file)
    chart(session.query(models.Ping).filter(models.Ping.date > since))
    plt.show()

