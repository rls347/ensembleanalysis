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
  pcpmin = []
  pcp = {}
  pcpz = {}
  for xdir in modeldirs:
      print xdir
      filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/bas*h5"))
      fil1 = hdf.File(filesrams[0], 'r')
      height = np.squeeze(fil1['z_coords'].value)
      pcp0 = np.sum(np.squeeze(fil1['tracer002'].value),1)  
      pcp0z = np.sum(pcp0,1)
      numfiles = len(filesrams)
      pcp[xdir] = []
      pcpz[xdir] = []
      for i in range(numfiles):
          fil = hdf.File(filesrams[i], 'r')
          d2 = np.sum(np.squeeze(fil['tracer002'].value),1)
          d1 = np.sum(d2,1)
          pcp[xdir].append(d2-pcp0)
          pcpz[xdir].append(d1-pcp0z)
          
        
      tmppcp = np.asarray(pcp[xdir])
      pcpmax.append(np.max(tmppcp))
      pcpmin.append(np.min(tmppcp))
      
            
  maxpcp = np.max(np.asarray(pcpmax))
  minpcp = np.min(np.asarray(pcpmin))  
  levels=np.linspace(minpcp,maxpcp,20)
  xs = np.arange(tmppcp.shape[2])*(100./tmppcp.shape[2])

  for i in range(numfiles):
      outi = str(i*5)
      if i < 2:
         outi = '0'+outi
      if i < 20:
         outi = '0'+outi 

      fig = plt.figure()
      z2 = []
      for xdir in modeldirs:
          z2.append(np.asarray(pcp[xdir])[i,:,:] * 25000.0)

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
      cbar.set_label('#/cm$^2$')
      plt.suptitle('Total Tracer Concentration'+str(i*5) + ' min', size = 20)
      plt.savefig('../plots/tracer2integral'+case+outi+'.png')
      plt.close(fig)

  os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/tracer2integral"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/tracer2integral"+case+".mp4") 
  os.system("rm ../plots/tracer2integral"+case+"*.png")


  for i in range(numfiles):
      outi = str(i*5)
      if i < 2:
         outi = '0'+outi
      if i < 20:
         outi = '0'+outi 

      fig = plt.figure()
      z2 = []
      for xdir in modeldirs:
          z2.append(np.asarray(pcpz[xdir])[i,:] * 25000.0 * 25000.0)

      for t in range(25):
          plt.plot(z2[t],height,color = 'black', linewidth = 2)
          plt.ylim(0,18000)
          plt.ylabel('Height (m)')
          plt.xlabel('#/cm')
      plt.title('Total Tracer Concentration'+str(i*5) + ' min', size = 20)
      plt.savefig('../plots/tracer2vertical'+case+outi+'.png')
      plt.close(fig)

  os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/tracer2vertical"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/tracer2vertical"+case+".mp4") 
  os.system("rm ../plots/tracer2vertical"+case+"*.png")
  outfile = case+"-2dtracer2int.npz"
  np.savez(outfile, **pcpz)



