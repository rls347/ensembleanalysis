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

cloudtops = {}

for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"/*h5")) 
	nfiles = len(files)
	times = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
#		cond = np.squeeze(fil['rain'].value+fil['cloud'].value+fil['drizzle'].value)/1000.
		cond = np.squeeze(fil['pristine'].value+fil['snow'].value+fil['aggregates'].value+fil['graupel'].value+fil['hail'].value)/1000.
		print xdir, f
		rho = (100*np.squeeze(fil['press'].value)) /(287 * np.squeeze(fil['tempk'].value))
		height = fil['z_coords'].value
		dz = np.zeros_like(height)
		dz[0:-1] = np.diff(height)
		dz[-1]=dz[-2]
		height5km = np.argmin(height-5000)
		var3d = cond[height5km:,:,:] * rho[height5km:,:,:] * dz[height5km:,None,None]
		ct = np.sum(var3d,0)
		times.append(ct)
	cloudtops[xdir] = np.asarray(times)
	#print xdir, np.max(cloudtops[xdir])

outfile = 'revuintabove5kmice.npz'
np.savez(outfile, **cloudtops)

#cloudtops = np.load('revuintcond.npz')
#for xdir in modeldirs:
#	ct = cloudtops[xdir]
#	ts = np.arange(nfiles)/2.
#	timeseries = np.zeros(nfiles)
#	for i in range(nfiles):
#		timeseries[i] = np.sum(ct[i,:,:])
#	plt.plot(ts,timeseries,linewidth = 3)
#	plt.ylabel('Total Condensate')
#	plt.xlabel('Time (min)')
#	plt.savefig('/nobackup/rstorer/plots/'+xdir+'totalcondintrevu.png')
#	plt.clf()
#	print xdir

