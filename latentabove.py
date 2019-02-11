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
onefile = '/nobackup/rstorer/convperts/growing/feb23-control/feb23-control-growing-001.h5'
fil = hdf.File(onefile, 'r')
height = fil['z_coords'].value
fil.close()
dz = np.zeros_like(height)
dz[0:-1]=height[1:]-height[:-1]
dz[-1]=dz[-2]

cp = 1004.
dti = 1./30.

cloudtops = {}

for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"/*h5")) 
	nfiles = len(files)
	times = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		lat = np.squeeze(fil['latheatfrzt'].value+fil['latheatvapt'].value)
		rho = (100*np.squeeze(fil['press'].value)) /(287 * np.squeeze(fil['tempk'].value))
		fil.close()
		var = lat*rho*cp*dti*dz[:,None,None]  # dtheta*cp=J/kg * rho = J/m3 *dz = J/m2 /30s = W/m2
		try:
			nz,ny,nx = lat.shape
		except:
			print 'wrong shape!', lat.shape
		height10km =0 #np.argmin(height-10000)
		var3d = var[height10km:,:,:]
		ct = np.sum(var3d,0)
		times.append(ct)
	cloudtops[xdir] = np.asarray(times)
	print xdir, np.max(cloudtops[xdir]), np.min(cloudtops[xdir]), np.mean(cloudtops[xdir])

outfile = 'growingintlatent.npz'
np.savez(outfile, **cloudtops)

#cloudtops = np.load('cloudtops.npz')
#for xdir in modeldirs:
#	ct = cloudtops[xdir]
#	nt,ny,nx = ct.shape
#	timeseries = np.max(np.max(ct,1),1)
#	ts = np.arange(nt)*5
#	plt.plot(ts,timeseries,linewidth = 3)
#	plt.ylabel('Max Cloud Top')
#	plt.xlabel('Time (min)')
#	plt.savefig('/nobackup/rstorer/plots/'+xdir+'CTtimeseries.png')
#	plt.clf()
#	print xdir

