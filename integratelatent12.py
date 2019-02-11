import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

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

for ch, chunk in enumerate(chunks):
	dti = 1./tdiff[ch]
	maindir = '/nobackup/rstorer/convperts/'+chunk+'/'
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
			print chunk, xdir, f
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
			print height5km,height8km,height10km
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
	#		var3d = var[height0km:,:,:] 
	#		ct = np.sum(var3d,0)
	#		times0.append(ct)
	
	
	#	out0[xdir] = np.asarray(times0)
		out5[xdir] = np.asarray(times5)
		out8[xdir] = np.asarray(times8)
		out10[xdir] = np.asarray(times10)
	
	outfile = chunk+'intabove5kmlatent.npz'
	np.savez(outfile, **out5)
	
	outfile = chunk+'intabove8kmlatent.npz'
	np.savez(outfile, **out8)
	
	outfile = chunk+'intabove10kmlatent.npz'
	np.savez(outfile, **out10)
	
	#outfile = chunk+'intlatent.npz'
	#np.savez(outfile, **out0)
	
