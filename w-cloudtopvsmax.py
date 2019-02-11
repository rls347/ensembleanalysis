import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/mature/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

columnmaxw = np.load('/nobackup/rstorer/filesnpz/maturecolumnmaxw.npz')
cloudtopw = np.load('/nobackup/rstorer/filesnpz/maturecloudtopw.npz')
cloudtops = np.load('/nobackup/rstorer/filesnpz/maturecloudtops.npz')

#for xdir in modeldirs:
#	cw = cloudtopw[xdir]
#	mw = columnmaxw[xdir]
#	nt,ny,nx = cw.shape
#	for t in nt

allcw = []
allmw = []

for xdir in modeldirs:
	print xdir
	ct = cloudtops[xdir].flatten()
	cw = cloudtopw[xdir].flatten()
	mw = columnmaxw[xdir].flatten()

	maxw = mw[np.where(mw>5)]
	ctw = cw[np.where(mw>5)]
	ctt = ct[np.where(mw>5)]
	print maxw.shape
	allcw.append(ctw)
	allmw.append(maxw)

	plt.scatter(maxw,ctw)
plt.xlabel('Column Max W')
plt.ylabel('Cloud Top W')
plt.title('max w > 5')
plt.savefig('../plots/mature-w-columnvscloudtop.png')
plt.clf()
allmws = np.concatenate(allmw)
allcws = np.concatenate(allcw)
plt.hist2d(allmws,allcws, bins = (100,100))
plt.xlabel('Column Max W')
plt.ylabel('Cloud Top W')
plt.savefig('../plots/mature-w-heatmap-columnvscloudtop.png')

