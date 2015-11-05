#!/usr/bin/env python
import time
import shutil
import os
from heartbeat import heartbeat
from merkle import hashtree
from multiprocessing import Pool

srcdir = '/tmp/deploy'
srchash = {}

def hashdir(d):
	h = {}
	for x in os.listdir(d):
		#if x == 'alive':
		#	continue
		h[x] = hashtree.hashtreeify(os.path.join(d,x))['topdigest']
	return h

def merkledeploy(m):
	global srcdir
	global srchash
	dsthash = hashdir(os.path.join(heartbeat.TOPDIR,str(m)))
	if dsthash != srchash:
		common = set(srchash.keys()) & set(dsthash.keys())
		diffset = {x for x in common if srchash[x] != dsthash[x]}
		diffset |= set(srchash.keys()) - set(dsthash.keys())
		for x in diffset:
			shutil.copy(srcdir+x,os.path.join(heartbeat.TOPDIR,str(m),x))
	dsthash = hashdir(os.path.join(heartbeat.TOPDIR,str(m)))
	return dsthash == srchash
	
def deploymachine(m):
	if os.path.exists(os.path.join(heartbeat.TOPDIR,str(m),'alive')):
		if merkledeploy(m):
			return {m: True}
	return {m: False}

def deploymachines(newmachines):
	if newmachines:
		p = Pool()
		m = p.map(deploymachine,newmachines)
		s = {u for x in m for u in x if x[u]}
		p.close()
		p.join()
		return s
	return set()

if __name__ == '__main__':
	machines = int(raw_input('Enter the number of machines: '))
	recoverytime = int(raw_input('Enter the number of seconds taken by a failed machine to recover: '))
	srcdir = raw_input('Enter the source directory of deployment: ')
	heartbeat.startmachines(machines,recoverytime=recoverytime)
	heartbeat.startprobe()
	m = {x for x in range(machines)}
	pam = set()
	currentcycle = 1
	srchash = hashdir(srcdir)
	while m - pam:
		time.sleep(1)
		if not currentcycle % recoverytime:
			am = heartbeat.getalivemachines()
			nm = deploymachines(am - pam)
			pam |= nm
		currentcycle += 1
	print('deployed to ' + str(machines) + ' machines')
