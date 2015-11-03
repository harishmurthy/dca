#!/usr/bin/env python

import argparse
import cmd
import readline
import signal
import random
import sys
import os

TOPDIR = '/tmp/machines/'
_currentinterval = 1
_machines = 0
_failureratio = 0
_recoveryinterval = 0
_activemachines = set()
_deadmachines = set()
_failuretrend = []

def _failsomemachines():
    global _activemachines
    s = list(_activemachines)
    for i in range(_failureratio):
        m = random.choice(s)
        os.remove(os.path.join(TOPDIR,str(m),'alive'))

def _recovermachine(m):
    if not os.path.exists(TOPDIR+str(m)):
        os.mkdir(TOPDIR+str(m))
    with open(os.path.join(TOPDIR,str(m),'alive'),'w') as f:
        f.write('alive')

def _recoveralldead():
    global _deadmachines
    for i in _deadmachines:
        _recovermachine(i)

def _problealivemachines():
    global _activemachines
    global _deadmachines
    for root,machines,files in os.walk(TOPDIR,topdown=False):
        for m in machines:
            if os.path.exists(root+m+'/alive'):
                _activemachines.add(m)
                _deadmachines.discard(m)
            else:
                _activemachines.discard(m)
                _deadmachines.add(m)

def _signalhandler(signum, frame):
    global _currentinterval
    global _machines
    global _failureinterval
    global _recoveryinterval
    global _activemachines
    global _deadmachines
    global _failuretrend
    if not _currentinterval % 5:
        _failsomemachines()
    if not _currentinterval % _recoveryinterval:
        _recoveralldead()
    _problealivemachines()
    if len(_failuretrend) < 10:
        _failuretrend.append(len(_activemachines))
    else:
        _failuretrend[_currentinterval % 10] = len(_activemachines)
    _currentinterval += 1

class HeartBeatMonitor(cmd.Cmd):
    prompt = 'HeartBeatMonitor>'

    def help_add_machines(self):
        print('Add machines to the list of monitored. Usage: add_machines M1 M2 M3 ...')

    def do_add_machines(self,line):
        m = line.split(' ')
        for i in m:
            _recovermachine(i)

    def help_remove_machines(self):
        print('Remove machines from the list of monitored. Usage: remove_machines M1 M2 M3 ...')

    def do_remove_machines(self,line):
        global _activemachines
        global _deadmachines
        m = line.split(' ')
        for i in m:
            os.remove(os.path.join(TOPDIR,str(i),'alive'))
            os.rmdir(os.path.join(TOPDIR,str(i)))
            _activemachines.discard(i)
            _deadmachines.discard(i)

    def help_is_machine_alive(self):
        print('Checks and return TRUE is given machine is alive')

    def do_is_machine_alive(self,line):
        global _activemachines
        m = line.split(' ')[0]
        if m in _activemachines:
            print('True')
        else:
            print('False')

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
        for root,dirs,files in os.walk(TOPDIR,topdown=False):
            for i in files:
                os.remove(os.path.join(root,i))
            for i in dirs:
                os.rmdir(os.path.join(root,i))
        os.removedirs(TOPDIR)
        print('Bye.')
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("machines", help="Number of machines", type=int, metavar='N')
    parser.add_argument("failures", help="percentage of machines that will fail every 5 seconds", type=int, metavar='f')
    parser.add_argument("recoverytime", help="number of seconds taken by a failed machine to recover", type=int, metavar='t')
    args = parser.parse_args()
    _machines = args.machines
    _failureratio = _machines * args.failures / 100
    _recoveryinterval = args.recoverytime
    os.mkdir(TOPDIR)
    for i in range(_machines):
        _recovermachine(i)
    signal.signal(signal.SIGALRM, _signalhandler)
    signal.setitimer(signal.ITIMER_REAL,1,1)
    h = HeartBeatMonitor()
    h.cmdloop()
