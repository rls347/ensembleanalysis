import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation

maindir = '/nobackup/rstorer/convperts/growing/'
modeldirs = os.walk(maindir).next()[1]
xs = np.arange(400)*(100./400.)
for xdir in modeldirs:
	print xdir
	filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
	numfiles = len(filesrams)
	condabove8 = np.zeros(numfiles)
	for i in range(numfiles):
		fil = hdf.File(filesrams[i], 'r')
		w = np.squeeze(fil['w'].value)
		height = np.squeeze(fil['z_coords'].value)
		dz = np.zeros_like(height)
		dz[0:-1] = np.diff(height)
		dz[-1] = dz[-2]
		cond=np.squeeze(fil['total_cond'].value) * dz[:,None,None]
		z8 = np.argmin((np.abs(height-8000)))
		condabove8[i] = np.sum(cond[z8:,:,:])*250*250
	plt.plot(condabove8)
	plt.savefig('../plots/above8'+xdir+'.png')
	plt.clf()
