import numpy as np
import glob
import os
import matplotlib.pyplot as plt

cases = ['aug17','aug11','feb23']
perts = ['-control']
for i in range(1,25):
    perts.append('-pert'+str(i))

rhout = np.load('../filesnpz/rh.npz')

rhlow = {}
rhmid = {}
rhhigh = {}
cape = {}

for case in cases:
	for i in range(25):
		name = case+perts[i]
		rhlow[name] = rhout[name][0]
		rhmid[name] = rhout[name][1]
		rhhigh[name] = rhout[name][2]
		cape[name] = rhout[name][3]

np.savez('../filesnpz/rhlow.npz', **rhlow)
np.savez('../filesnpz/rhmid.npz', **rhmid)
np.savez('../filesnpz/rhhigh.npz', **rhhigh)
np.savez('../filesnpz/cape.npz', **cape)

