import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

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

cloudtops = {}

for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"*h5")) 
	nfiles = len(files)
	times = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		ref = np.squeeze(fil['reflectivity'].value)
		try:
			nz,ny,nx = ref.shape
		except:
			print 'wrong shape!', ref.shape
		ct = np.zeros((ny,nx))
		for i in range(ny):
			if np.max(ref[:,i,:]) > 0:
				for j in range(nx):
					try:
						tmp = height[ref[:,i,j]>0]
						ct[i,j] = np.max(tmp)
					except:
						ct[i,j] = 0
		times.append(ct)
	cloudtops[xdir] = np.asarray(times)
	print xdir, np.max(cloudtops[xdir]), np.min(cloudtops[xdir]), np.mean(cloudtops[xdir])

outfile = 'revuechotop0.npz'
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

