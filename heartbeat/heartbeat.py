#!/usr/bin/env python

import cmd
import signal
import random
import sys
import os
import math
from multiprocessing import Pool

TOPDIR = '/tmp/machines/'
_currentinterval = 1
_machines = set()
_failureratio = 0
_recoveryinterval = 0
_activemachines = set()
_deadmachines = set()
_failuretrend = []

def _failmachine(m):
    if os.path.exists(os.path.join(TOPDIR,str(m),'alive')):
        os.remove(os.path.join(TOPDIR,str(m),'alive'))

def _recovermachine(m):
    if not os.path.exists(TOPDIR+str(m)):
        os.mkdir(TOPDIR+str(m))
    if not os.path.exists(os.path.join(TOPDIR,str(m),'alive')):
        with open(os.path.join(TOPDIR,str(m),'alive'),'w') as f:
            f.write('alive')

def _probemachine(m):
    if os.path.exists(os.path.join(TOPDIR,str(m),'alive')):
        return {m: True}
    return {m: False}

def _failsomemachines(machines,failureratio):
    if machines:
        f = random.sample(machines,failureratio)
        p = Pool()
        m = p.map(_failmachine,f)
        p.close()
        p.join()
        return m

def _recoverdeadmachines(deadmachines):
    if deadmachines:
        p = Pool()
        p.map(_recovermachine,deadmachines)
        p.close()
        p.join()

def probeallmachines(machines):
    if machines:
        p = Pool()
        m = p.map(_probemachine,machines)
        p.close()
        p.join()
        return m

def getalivemachines():
    global _machines
    p = probeallmachines(_machines)
    activemachines = {u for x in p for u in x if x[u]}
    return activemachines

def signalhandler(signum, frame):
    global _currentinterval
    global _machines
    global _failureratio
    global _recoveryinterval
    global _activemachines
    global _deadmachines
    global _failuretrend
    p = probeallmachines(_machines)
    _activemachines = {u for x in p for u in x if x[u]}
    _deadmachines = _machines - _activemachines
    if not _currentinterval % 5:
        _failsomemachines(_machines,_failureratio)
    if not _currentinterval % _recoveryinterval:
        _recoverdeadmachines(_deadmachines)
    if len(_failuretrend) < 10:
        _failuretrend.append(len(_activemachines))
    else:
        _failuretrend[_currentinterval % 10] = len(_activemachines)
    _currentinterval += 1

def startmachines(nummachines,start=0):
    global _machines
    if not os.path.exists(TOPDIR):
        os.mkdir(TOPDIR)
    _machines = {x for x in range(nummachines)}
    if start:
        m = random.sample(_machines,start)
    else:
        m = _machines 
    for i in m:
        _recovermachine(i)

def startprobe():
    signal.signal(signal.SIGALRM, signalhandler)
    signal.setitimer(signal.ITIMER_REAL,1,1)

class HeartBeatMonitor(cmd.Cmd):
    prompt = 'HeartBeatMonitor>'

    def help_add_machines(self):
        print('Add machines to the list of monitored. Usage: add_machines M1 M2 M3 ...')

    def do_add_machines(self,line):
        global _machines
        global _activemachines
        global _deadmachines
        m = line.split(' ')
        for i in m:
            i = int(i)
            if i not in _machines:
                _machines.add(i)
                _recovermachine(i)
            else:
                print('Machine ' + str(i) + ' already present')

    def help_remove_machines(self):
        print('Remove machines from the list of monitored. Usage: remove_machines M1 M2 M3 ...')

    def do_remove_machines(self,line):
        global _machines
        m = line.split(' ')
        for i in m:
            i = int(i)
            if i in _machines:
                _machines.discard(i)
                os.remove(os.path.join(TOPDIR,str(i),'alive'))
                os.rmdir(os.path.join(TOPDIR,str(i)))
            else:
                print('Machine ' + str(i) + ' not present')


    def help_is_machine_alive(self):
        print('Checks and return TRUE is given machine is alive')

    def do_is_machine_alive(self,line):
        global _activemachines
        global _machines
        m = int(line.split(' ')[0])
        if m in _machines:
            if m in _activemachines:
                print('True')
            else:
                print('False')
        else:
            print('Machine not present')

    def help_num_machines_alive(self):
        print('Returns the number of machines currently alive')

    def do_num_machines_alive(self,line):
        global _activemachines
        print(str(len(_activemachines)))

    def help_failure_trend(self):
        print('Returns count of machines that were alive over past 10 probe cycles')

    def do_failure_trend(self,line):
        global _failuretrend
        print(str(_failuretrend))

    def do_quit(self,line):
        global _machines
        global _activemachines
        global _deadmachines
        signal.setitimer(signal.ITIMER_REAL,0,0)
        _machines.clear()
        for root,dirs,files in os.walk(TOPDIR,topdown=False):
            for i in files:
                os.remove(os.path.join(root,i))
            for i in dirs:
                os.rmdir(os.path.join(root,i))
        os.removedirs(TOPDIR)
        print('Bye.')
        sys.exit(0)

if __name__ == "__main__":
    rinput = raw_input('Enter the number of machines: ')
    machines = int(rinput)
    rinput = raw_input('Enter the percentage of machines that will fail every 5 seconds: ')
    _failureratio = int(math.ceil(int(rinput) * machines / 100.0))
    rinput = raw_input('Enter the number of seconds taken by a failed machine to recover: ')
    _recoveryinterval = int(rinput)
    startmachines(machines)
    startprobe()
    HeartBeatMonitor().cmdloop()
