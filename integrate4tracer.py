import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

out0 = {}
out5 = {}
out8 = {}
out10 = {}


for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"/*h5")) 
	nfiles = len(files)
	times0 = []
	times5 = []
	times8 = []
	times10 = []

	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		cond = np.squeeze(fil['tracer002'].value) * 100. * 100. * 100.
		print xdir, f
		height = fil['z_coords'].value
		dz = np.zeros_like(height)
		dz[0:-1] = np.diff(height)
		dz[-1]=dz[-2]
		height5km = np.argmin(np.abs(height-5000))
		height8km = np.argmin(np.abs(height-8000))
		height10km = np.argmin(np.abs(height-10000))
		height0km = 0 
		print height5km, height8km, height10km
		var3d = cond[height5km:,:,:] * dz[height5km:,None,None]
		ct = np.sum(var3d,0)
		times5.append(ct)
		var3d = cond[height8km:,:,:] * dz[height8km:,None,None]
		ct = np.sum(var3d,0)
		times8.append(ct)
		var3d = cond[height10km:,:,:] * dz[height10km:,None,None]
		ct = np.sum(var3d,0)
		times10.append(ct)
#		var3d = cond[height0km:,:,:] * dz[height0km:,None,None]
#		ct = np.sum(var3d,0)
#		times0.append(ct)


#	out0[xdir] = np.asarray(times0)
	out5[xdir] = np.asarray(times5)
	out8[xdir] = np.asarray(times8)
	out10[xdir] = np.asarray(times10)

outfile = 'revuintabove5kmtracer2.npz'
np.savez(outfile, **out5)

outfile = 'revuintabove8kmtracer2.npz'
np.savez(outfile, **out8)

outfile = 'revuintabove10kmtracer2.npz'
np.savez(outfile, **out10)

#outfile = 'revuinttracer2.npz'
#np.savez(outfile, **out0)

