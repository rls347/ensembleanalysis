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
chunks = ['growing']
for chunk in chunks:
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
	#		cond = np.squeeze(fil['rain'].value+fil['cloud'].value+fil['drizzle'].value)/1000.
	#		cond = np.squeeze(fil['pristine'].value+fil['snow'].value+fil['aggregates'].value+fil['graupel'].value+fil['hail'].value)/1000.
	#		cond = np.squeeze(fil['total_cond'].value)/1000.
			cond = np.squeeze(fil['vapor'].value)/1000.
			print chunk, xdir, f
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
			var3d = cond[height5km:,:,:] * rho[height5km:,:,:] * dz[height5km:,None,None]
			ct = np.sum(var3d,0)
			times5.append(ct)
			var3d = cond[height8km:,:,:] * rho[height8km:,:,:] * dz[height8km:,None,None]
			ct = np.sum(var3d,0)
			times8.append(ct)
			var3d = cond[height10km:,:,:] * rho[height10km:,:,:] * dz[height10km:,None,None]
			ct = np.sum(var3d,0)
			times10.append(ct)
	#		var3d = cond[height0km:,:,:] * rho[height0km:,:,:] * dz[height0km:,None,None]
	#		ct = np.sum(var3d,0)
	#		times0.append(ct)
	
	
	#	out0[xdir] = np.asarray(times0)
		out5[xdir] = np.asarray(times5)
		out8[xdir] = np.asarray(times8)
		out10[xdir] = np.asarray(times10)
	
	outfile = chunk+'intabove5kmvapor.npz'
	np.savez(outfile, **out5)
	
	outfile = chunk+'intabove8kmvapor.npz'
	np.savez(outfile, **out8)
	
	outfile = chunk+'intabove10kmvapor.npz'
	np.savez(outfile, **out10)
	
	#outfile = chunk+'intvapor.npz'
	#np.savez(outfile, **out0)
	
