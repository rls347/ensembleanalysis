import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

def onerun(maindir,xdir,height):
	print xdir
	files = sorted(glob.glob(maindir+xdir+"*h5"))
	nfiles = len(files)
	times0 = []
	times5 = []
	times10 = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		ref = np.squeeze(fil['reflectivity'].value)
		try:
			nz,ny,nx = ref.shape
		except:
			print 'wrong shape!', ref.shape
		ct0 = np.zeros((ny,nx))
		ct5 = np.zeros((ny,nx))
		ct10 = np.zeros((ny,nx))
		for i in range(ny):
			if np.max(ref[:,i,:]) > 0:
				for j in range(nx):
					try:
						tmp = height[ref[:,i,j]>0]
						ct0[i,j] = np.max(tmp)
					except:
						ct0[i,j] = 0
			if np.max(ref[:,i,:]) > 5:
				for j in range(nx):
					try:
						tmp = height[ref[:,i,j]>5]
						ct5[i,j] = np.max(tmp)
					except:
						ct5[i,j] = 0
			if np.max(ref[:,i,:]) > 10:
				for j in range(nx):
					try:
						tmp = height[ref[:,i,j]>10]
						ct10[i,j] = np.max(tmp)
					except:
						ct10[i,j] = 0
		times0.append(ct0)
		times5.append(ct5)
		times10.append(ct10)
	return np.asarray(times0), np.asarray(times5), np.asarray(times10)

cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/revu/quickbeam/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))
onefile = '/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5'
fil = hdf.File(onefile, 'r')
height = fil['z_coords'].value
fil.close()

et0 = {}
et5 = {}
et10 = {}

for xdir in modeldirs:
	times0, times5, times10 = onerun(maindir,xdir,height)
	et0[xdir] = times0
	et5[xdir] = times5
	et10[xdir] = times10

outfile = 'revuechotop0.npz'
np.savez(outfile, **et0)

outfile = 'revuechotop5.npz'
np.savez(outfile, **et5)

outfile = 'revuechotop10.npz'
np.savez(outfile, **et10)
