import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

columnmaxw = np.load('/nobackup/rstorer/filesnpz/2d/columnmaxw.npz')
echo10 = np.load('/nobackup/rstorer/filesnpz/revuechotop10.npz')
echo5 = np.load('/nobackup/rstorer/filesnpz/revuechotop5.npz')
echo0 = np.load('/nobackup/rstorer/filesnpz/revuechotop0.npz')


alle0 = []
alle5 = []
alle10 = []
allmw = []

for xdir in modeldirs:
	print xdir
	nt,nx,ny = columnmaxw[xdir].shape
	for ti in range(nt-1):
		mw = columnmaxw[xdir][ti].flatten()
		e10 = echo10[xdir][ti+1].flatten() - echo10[xdir][ti].flatten()
		e5 = echo5[xdir][ti+1].flatten() - echo5[xdir][ti+1].flatten()
		e0 = echo0[xdir][ti+1].flatten() - echo0[xdir][ti+1].flatten()

		maxw = mw[np.where(mw>1)]
		e10w = e10[np.where(mw>1)]
		e5w = e5[np.where(mw>1)]
		e0w = e0[np.where(mw>1)]
	
		alle0.append(e0w)
		alle5.append(e5w)
		alle10.append(e10w)
		allmw.append(maxw)

allmws = np.concatenate(allmw)
alle10s = np.concatenate(alle10)
alle5s = np.concatenate(alle5)
alle0s = np.concatenate(alle0)

plt.scatter(allmws,alle10s)
plt.xlabel('Column Max W')
plt.ylabel('10dbz Echo Top Height')
plt.title('max w vs 10dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho10diff.png')
plt.clf()
plt.scatter(allmws,alle5s)
plt.xlabel('Column Max W')
plt.ylabel('5dbz Echo Top Height')
plt.title('max w vs 5dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho5diff.png')
plt.clf()
plt.scatter(allmws,alle0s)
plt.xlabel('Column Max W')
plt.ylabel('0dbz Echo Top Height')
plt.title('max w vs 0dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho0diff.png')
plt.clf()

plt.hist2d(allmws,alle10s, bins = (100,100))
plt.xlabel('Column Max W')
plt.ylabel('10dbz Echo Top Height')
plt.title('max w vs 10dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho10diff-hist.png')
plt.clf()
plt.hist2d(allmws,alle5s, bins = (100,100))
plt.xlabel('Column Max W')
plt.ylabel('5dbz Echo Top Height')
plt.title('max w vs 5dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho5diff-hist.png')
plt.clf()
plt.hist2d(allmws,alle0s, bins = (100,100))
plt.xlabel('Column Max W')
plt.ylabel('0dbz Echo Top Height')
plt.title('max w vs 0dbz height (w>1)')
plt.savefig('../plots/revu-w-columnvsecho0diff-hist.png')
plt.clf()
