import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation


maindir = '/nobackup/rstorer/convperts/mature/'
modeldirs = ['control']
#for i in range(1,25):
#    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']
case = cases[0]

#xval = [166,164,163]

#0 60
#163 243

#aug11-control
#0 60
#164 256

#feb23-control
#0 60
#166 247

for case in cases:
  pcpmax = []
  pcp = {}
  for xdir in modeldirs:
      print xdir
      pcp[xdir]=[]
      filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/"+case+"*h5"))
      numfiles = len(filesrams)
      for i in range(5):
          fil = hdf.File(filesrams[i], 'r')
          slicevar = np.squeeze(fil['vapliqt'].value[:,:,160:170,:])+np.squeeze(fil['nuccldrt'].value[:,:,160:170,:])
          print slicevar.shape
          pcp[xdir].append(np.mean(slicevar,1))
  fil2 = hdf.File('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','r')
  height = np.squeeze(fil2['z_coords'].value)
  fil2.close()
  xs = np.arange(400)*.25
  maxvar = np.max(np.asarray(pcp[xdir]))
  minvar = np.min(np.asarray(pcp[xdir]))
#  levels=np.logspace(-2,1.3,20)
  levels = np.linspace(minvar,maxvar,20)
  for i in range(5):
      outi = str(i)
      if i < 10:
         outi = '0'+outi

      fig = plt.figure()
      z2 = pcp[xdir][i]
      f = plt.contourf(xs, height, z2, levels = levels)
      if height.max() > 20000:
      	plt.ylim(0,18000)
      if height.max() < 50:
      	plt.ylim(0,18)
      cbar = plt.colorbar(f)
      plt.suptitle('vaportoliq '+str(i*30) + ' s', size = 20)
      plt.savefig('../plots/vaportoliq'+case+outi+'.png')
      plt.close()

#  os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/latentheat"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/latentheat"+case+".mp4") 
#  os.system("rm ../plots/tracer2max"+case+"*.png")


