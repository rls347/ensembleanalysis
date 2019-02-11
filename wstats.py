import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

def calculateonedir(maindir, xdir):
	files = sorted(glob.glob(maindir+xdir+"/*h5"))
	nfiles = len(files)
	times = []
	times5 = []
	mintimes5 = []
	mintimes = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		w = np.squeeze(fil['w'].value)
		height = fil['z_coords'].value
		dz = np.zeros_like(height)
		dz[0:-1] = np.diff(height)
		dz[-1]=dz[-2]
		height5km = np.argmin(np.abs(height-5000))
		var3d = w[height5km:,:,:]
		ct = np.max(var3d,0)
		times5.append(ct)
		ct = np.max(w,0)
		times.append(ct)
		ct = np.min(var3d,0)
		mintimes5.append(ct)
		ct = np.min(w,0)
		mintimes.append(ct)
	print np.max(np.asarray(times5))
	
	return np.asarray(times5), np.asarray(times), np.asarray(mintimes5), np.asarray(mintimes)


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
chunks = ['revu']

for ch, chunk in enumerate(chunks):
	dti = 1./tdiff[ch]
	maindir = '/nobackup/rstorer/convperts/'+chunk+'/'
	outmin5 = {}
	outmax5 = {}
	outmin = {}
	outmax = {}	
	
	for xdir in modeldirs:
		print chunk, xdir
		outmax5[xdir], outmax[xdir], outmin5[xdir], outmin[xdir] = calculateonedir(maindir, xdir)
	
	outfile = chunk+'-maxw.npz'
	np.savez(outfile, **outmax)
	
	outfile = chunk+'-maxwabove5km.npz'
	np.savez(outfile, **outmax5)
	
	outfile = chunk+'-minw.npz'
	np.savez(outfile, **outmin)
	
	outfile = chunk+'-minwabove5km.npz'
	np.savez(outfile, **outmin5)
	
