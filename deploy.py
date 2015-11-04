#!/usr/bin/env python

from heartbeat import heartbeat
from merkle import hashtree

if __name__ == '__main__':
    rinput = raw_input('Enter the number of machines: ')
    _machines = {x for x in range(int(rinput))}
    rinput = raw_input('Enter the number of seconds taken by a failed machine to recover: ')
    _recoveryinterval = int(rinput)
    heartbeat.startprobe()

