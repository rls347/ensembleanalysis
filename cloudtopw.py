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

cloudtops = np.load('../filesnpz/growingcloudtops.npz')
ctw = {}

nz = 82
ncol =400*400

for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"/bas*h5")) 
	nfiles = len(files)
	ctw[xdir] = np.zeros_like(cloudtops[xdir])
	for f in range(nfiles):
		ct = np.reshape(cloudtops[xdir][f,:,:],ncol)
		fil = hdf.File(files[f],'r')
		w = np.reshape(np.squeeze(fil['w'].value),(nz,ncol))
		ww = np.zeros_like(ct)
		height = np.squeeze(fil['z_coords'].value)
		height[0]=0
		for col in range(ncol):
			ww[col]=w[np.where(height==ct[col]),col]
		ctw[xdir][f,:,:] = np.reshape(ww,(400,400))
	print np.min(ctw[xdir]), np.max(ctw[xdir])


outfile = 'growingcloudtopw.npz'
np.savez(outfile, **ctw)



