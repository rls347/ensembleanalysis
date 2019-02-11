import numpy as np
import h5py as hdf
import glob
import os
import copy
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def precipstats(maindir, modeldirs, dirout):
	totalpcprates = {}
	totalpcp = {}
	convpcprates = {}
	allrates = {}
	allconv = {}
	for xdir in modeldirs:
		print xdir
		filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
		numfiles = len(filesrams)
		pcprate = []
		totpcp = []
		for i in range(numfiles):
			fil = hdf.File(filesrams[i], 'r')
			pcprate.append(np.squeeze(fil['pcprate'].value))
			totpcp.append(np.squeeze(fil['totpcp'].value))
		totpcp = np.asarray(totpcp)
		pcprate = np.asarray(pcprate)
		convrate = copy.deepcopy(pcprate)
		lowpcp = np.where(pcprate<25.4)
		convrate[lowpcp] = 0.0

		allrates[xdir] = copy.deepcopy(pcprate)
		allconv[xdir] = copy.deepcopy(convrate)

		pcprate = pcprate*(5./60.)
		convrate = convrate*(5./60.)

		print 'pcprate: ',np.sum(pcprate)
		print 'convective: ', np.sum(convrate)
		print 'totpcp: ',np.sum(totpcp[-1,:,:])
		print '  '

		totalpcprates[xdir] = np.sum(pcprate)
		convpcprates[xdir] = np.sum(convrate)
		totalpcp[xdir] = np.sum(totpcp[-1,:,:])
	np.savez('convprecipmm.npz', **convpcprates)	
	np.savez('totpcpmm.npz', **totalpcp)
	np.savez('totalpcpratesmm.npz', **totalpcprates)
	np.savez('allpcprates.npz', **allrates)
	np.savez('allconvrates.npz', **allconv)

########################################

maindir = '/nobackup/rstorer/convperts/revu/'
#modeldirs = ['aug11-control','aug17-control','feb23-control']
cases = ['aug11','aug17','feb23']
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))
dirout = '/nobackup/rstorer/plots/'

precipstats(maindir, modeldirs, dirout)

