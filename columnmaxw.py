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

cloudtops = {}

for xdir in modeldirs:
	files = sorted(glob.glob(maindir+xdir+"/bas*h5")) 
	nfiles = len(files)
	times = []
	for f in range(nfiles):
		fil = hdf.File(files[f],'r')
		w = np.max(np.squeeze(fil['w'].value),0)
		times.append(w)
	cloudtops[xdir] = np.asarray(times)
	print xdir, np.max(cloudtops[xdir])

outfile = 'growingcolumnmaxw.npz'
np.savez(outfile, **cloudtops)

maindir = '/nobackup/rstorer/convperts/growing/'
modeldirs = os.walk(maindir).next()[1]
dx = 250
dy = 250
dt = 300

#modeldirs = ['aug11-control']
#columnmaxw = np.load('columnmaxw.npz')
#cloudtops = np.load('cloudtops.npz')

#for xdir in modeldirs:
	
#	cw = columnmaxw[xdir]
#	ct = cloudtops[xdir]
#	nt,ny,nx = cw.shape
#	ys = []
#	xs = []
#	ws = []
#	for i in range(nt):
#		a = cw[i,:,:]
#		b = ct[i,:,:]
#		if a.max() > 1:
#			val = np.unravel_index(b.argmax(), b.shape)
#			ys.append(val[0])
#			xs.append(val[1])
#			ws.append(a.max())
	#		print val, a.max(), b[val[0],val[1]], b.max() 

#	print np.mean(np.asarray(ys)), np.max(np.asarray(ys)), np.min(np.asarray(ys))
#	print np.mean(np.asarray(xs)), np.max(np.asarray(xs)), np.min(np.asarray(xs))

