import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation

'''Creates an XZ slice of averaged condensate for each time, then makes a movie'''

maindir = '/nobackup/rstorer/convperts/revu30s/'
#modeldirs = os.walk(maindir).next()[1]
modeldirs = ['control']
for i in range(1,25):
    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']
case = cases[0]
pcp = {}
for xdir in modeldirs:

	print xdir 
	filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/bas*h5"))
	numfiles = len(filesrams)
	pcp[xdir] = []
	for i in range(numfiles):
  fil = hdf.File(filesrams[i], 'r')
  			pcp[xdir].append(np.max(np.squeeze(fil['total_cond'].value),1))
  			height = np.squeeze(fil['z_coords'].value)
  		xs = np.arange(400)*(100./400.)        
         
  		z2 = []
  		levels=np.logspace(-2,1.3,20)
  		for i in range(numfiles):
			outi = str(i*5)
      		if i < 2:
         		outi = '0'+outi
      		if i < 20:
         		outi = '0'+outi 

      		fig = plt.figure()
      		z2 = []
      		for xdir in modeldirs:
          		z2.append(np.asarray(pcp[xdir])[i,:,:])

      		fig, axes = plt.subplots(nrows=5, ncols=5, sharex=True, sharey=True)

      		for t in range(25):
          		try:
					ax = axes.flat[t]
					f = ax.contourf(xs, height, z2[t], levels = levels)
					if height.max() > 20000:
						plt.ylim(0,17000)
					if height.max() < 50:
						plt.ylim(0,17)
          		except:
					print 'time ', t, 'has no value in ', xdir
      		cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
      		cbar = plt.colorbar(f, cax=cax,**kw)
      		plt.suptitle('Max Condensate '+str(i*5) + ' min', size = 20)
      		plt.savefig('../plots/maxcond'+case+outi+'.png')
      		plt.close()

  	os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/maxcond"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/maxcond"+case+"-30s-growing.mp4")   
  	os.system("rm ../plots/maxcond"+case+"*.png")

