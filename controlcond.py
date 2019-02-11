import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation


maindir = '/nobackup/rstorer/convperts/revu/'

labels = ['Aug 17','Aug 11','Feb 23']
cases = ['aug17-control','aug11-control','feb23-control']
pcpmax = []
pcp = {}
allnumfiles = []
for xdir in cases:
  print xdir
  filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
  numfiles = len(filesrams)
  pcp[xdir] = []
  allnumfiles.append(numfiles)
  for i in range(numfiles):
      fil = hdf.File(filesrams[i], 'r')
      pcp[xdir].append(np.max(np.squeeze(fil['total_cond'].value),1))
    
  tmppcp = np.asarray(pcp[xdir])
  pcpmax.append(np.max(tmppcp))
  height = np.squeeze(fil['z_coords'].value)
  xs = np.arange(tmppcp.shape[2])*(100./tmppcp.shape[2])
        
maxpcp = np.max(np.asarray(pcpmax))

numfiles = np.max(np.asarray(allnumfiles))
print numfiles
for i in range(numfiles):
  outi = str(i*5)
  if i < 2:
     outi = '0'+outi
  if i < 20:
     outi = '0'+outi 

  fig = plt.figure()
  z2 = []
  for t,xdir in enumerate (cases):
    if i<allnumfiles[t]:
      z2.append(np.asarray(pcp[xdir])[i,:,:])
    else:
      z2.append(np.asarray(pcp[xdir])[-1,:,:])

  fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
  levels=np.logspace(-2,1.3,20) 
  for t,xdir in enumerate(cases):
      ax = axes.flat[t]
      f = ax.contourf(xs, height, z2[t], levels = levels)
      if height.max() > 20000:
          plt.ylim(0,17000)
      if height.max() < 50:
          plt.ylim(0,17)
  cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
  cbar = plt.colorbar(f, cax=cax,**kw)
  cbar.set_label('g/kg', rotation = 90)
  plt.suptitle('Max Condensate '+str(i*5) + ' min', size = 20)
  plt.savefig('../plots/controlcond'+outi+'.png')
  plt.close()

os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/controlcond*.png' -c:v libx264 -pix_fmt yuv420p ../plots/controlcond.mp4")
os.system("rm ../plots/controlcond*.png")



