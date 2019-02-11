import matplotlib.pyplot as plt
import copy
import numpy as np
import h5py as hdf
import glob
import os

def calculateonedir(maindir, xdir):
	files = sorted(glob.glob(maindir+xdir+"/*h5"))
	nfiles = len(files)
	times0 = []
	times5 = []
	times8 = []
	times10 = []
	dti = 1./300.

	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		lat = np.squeeze(fil['latheatfrzt'].value+fil['latheatvapt'].value)
		rho = (100*np.squeeze(fil['press'].value)) /(287 * np.squeeze(fil['tempk'].value))
		height = fil['z_coords'].value
		dz = np.zeros_like(height)
		dz[0:-1] = np.diff(height)
		dz[-1]=dz[-2]
		height5km = np.argmin(np.abs(height-5000))
		height8km = np.argmin(np.abs(height-8000))
		height10km = np.argmin(np.abs(height-10000))
		height0km = 0
		var = lat*rho*cp*dti*dz[:,None,None]
		var3d = var[height5km:,:,:]
		ct = np.sum(var3d,0)
		times5.append(ct)
		var3d = var[height8km:,:,:]
		ct = np.sum(var3d,0)
		times8.append(ct)
		var3d = var[height10km:,:,:]
		ct = np.sum(var3d,0)
		times10.append(ct)
		var3d = var[height0km:,:,:] 
		ct = np.sum(var3d,0)
		times0.append(ct)
	print np.max(np.asarray(times5))
	
	return np.asarray(times0), np.asarray(times5), np.asarray(times8), np.asarray(times10)


cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/growing/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

chunks = ['revu','mature','growing']
tdiff = [300.,30.,30.]
cp = 1004.
chunk = 'revu'
maindir = '/nobackup/rstorer/convperts/'+chunk+'/'
out0= np.load('/nobackup/rstorer/filesnpz/revuintlatent.npz')
out5= np.load('/nobackup/rstorer/filesnpz/revuintabove5kmlatent.npz')
out8= np.load('/nobackup/rstorer/filesnpz/revuintabove8kmlatent.npz')
out10= np.load('/nobackup/rstorer/filesnpz/revuintabove10kmlatent.npz')

copyout5 = {}
copyout8 = {}
copyout0 = {}
copyout10 = {}

for xdir in modeldirs:
	copyout0[xdir] = copy.deepcopy(out0[xdir])
	copyout5[xdir] = copy.deepcopy(out5[xdir])
	copyout8[xdir] = copy.deepcopy(out8[xdir])
	copyout10[xdir] = copy.deepcopy(out10[xdir])


modeldirs = ['aug11-pert8','aug11-pert9']

for xdir in modeldirs:
	t1,t2,t3,t4 = calculateonedir(maindir,xdir)
	copyout0[xdir] = t1
	copyout5[xdir] = t2 
	copyout8[xdir] = t3
	copyout10[xdir] = t4 
	
outfile = 'revuintabove5kmlatent.npz'
np.savez(outfile, **out5)

outfile = 'revuintabove8kmlatent.npz'
np.savez(outfile, **out8)

outfile = 'revuintabove10kmlatent.npz'
np.savez(outfile, **out10)

outfile = 'revuintlatent.npz'
np.savez(outfile, **out0)


