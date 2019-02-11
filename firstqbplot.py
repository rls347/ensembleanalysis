import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation


maindir = '/nobackup/rstorer/convperts/mature/quickbeam/'
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
  height10 = []
  fil2 = hdf.File('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','r')
  height = np.squeeze(fil2['z_coords'].value)
  for xdir in modeldirs:
      print xdir
      filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"*h5"))
      numfiles = len(filesrams)
      pcp[xdir] = []
      for i in range(numfiles):
          fil = hdf.File(filesrams[i], 'r')
          slicevar = np.squeeze(fil['reflectivity'].value[:,160:170,:])
          pcp[xdir].append(np.mean(slicevar,1))
          tmp = pcp[xdir][i]
          loc = np.where(tmp>10)
          height10.append(height[np.max(loc[0])])

      


  fil2.close()
  xs = np.arange(400)*.25
            

  levels=np.linspace(-20,50,20)

#  for i in range(numfiles):
#      outi = str(i)
#      if i < 10:
#         outi = '0'+outi
#
#      fig = plt.figure()
#      z2 = pcp[xdir][i]
#      f = plt.contourf(xs, height, z2, levels = levels)
#      if height.max() > 20000:
#      	plt.ylim(0,18000)
#      if height.max() < 50:
#      	plt.ylim(0,18)
#      cbar = plt.colorbar(f)
#      cbar.set_label('dbz')
#      plt.suptitle('Radar Reflectivity'+str(i*30) + ' s', size = 20)
#      plt.savefig('../plots/radarslice'+case+outi+'.png')
#      plt.close()
  plt.plot(height10,linewidth = 3)
  plt.savefig('../plots/dbz10'+case+'.png')
  plt.close()
#  os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/radarslice"+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/radarslice"+case+".mp4") 
#  os.system("rm ../plots/tracer2max"+case+"*.png")


