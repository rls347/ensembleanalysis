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
modeldirs = ['control']
for i in range(1,25):
    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']
case = cases[0]


for case in cases:
  pcpmax = []
  pcp = {}
  for xdir in modeldirs:
      print xdir
      filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/*h5"))
      numfiles = len(filesrams)
      pcp[xdir] = []
      for i in range(numfiles):
          fil = hdf.File(filesrams[i], 'r')
          pcp[xdir].append(np.max(np.squeeze(fil['tracer002'].value),1))
        
      tmppcp = np.asarray(pcp[xdir])
      pcpmax.append(np.max(tmppcp))
      height = np.squeeze(fil['z_coords'].value)
      xs = np.arange(tmppcp.shape[2])*(100./tmppcp.shape[2])
            
  maxpcp = np.max(np.asarray(pcpmax))
         
  #fig = plt.figure()

  levels=np.linspace(0,maxpcp,20)


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
              varplot = z2[t]
              varplot[varplot<1]=np.log(0)
              f = ax.contourf(xs, height, z2[t], levels = levels)
              if height.max() > 20000:
                  plt.ylim(0,17000)
              if height.max() < 50:
                  plt.ylim(0,17)
          except:
              print 'time ', t, 'has no value in ', xdir
      cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
      cbar = plt.colorbar(f, cax=cax,**kw)
      cbar.set_label('#/cm$^3$')
      plt.suptitle('Max Tracer Concentration'+str(i*5) + ' min', size = 20)
      plt.savefig('../plots/tracer2max'+case+outi+'.png')
      plt.close()
      plt.clf()
  os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/tracer2max"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/tracer2max"+case+".mp4") 
#  os.system("rm ../plots/tracer2max"+case+"*.png")


