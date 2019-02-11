import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation


def getmaxw(maindir, xdir):
    filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
    numfiles = len(filesrams)
    ws = np.zeros(numfiles)
    for i in range(numfiles):
        fil = hdf.File(filesrams[i], 'r')
        ws[i] = np.max(fil['w'].value)        
    return(ws)
    
def getmaxcondvars(maindir, xdir):
    filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
    numfiles = len(filesrams)
    pcp= []
    for i in range(numfiles):
        fil = hdf.File(filesrams[i], 'r')
        pcp.append(np.max(np.squeeze(fil['total_cond'].value),1))
    tmppcp = np.asarray(pcp)
    height = np.squeeze(fil['z_coords'].value)
    xs = np.arange(tmppcp.shape[2])*(100./tmppcp.shape[2])
    maxpcp = np.max(tmppcp)
    
    return tmppcp, height, xs, maxpcp, numfiles
    

cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = []
for case in cases:
  modeldirs.append(case+'-control')
  for i in range(1,25):
    modeldirs.append(case+'-pert'+str(i))

modeldirs = ['feb23-control']

for xdir in modeldirs:  
    print xdir
    maxw = getmaxw(maindir, xdir)
    pcp, height, xs, maxpcp, numfiles = getmaxcondvars(maindir, xdir)
    levels=np.linspace(0,maxpcp,20)
    
    for i in range(numfiles):
      outi = str(i*5)
      if i < 2:
         outi = '0'+outi
      if i < 20:
         outi = '0'+outi

      fig = plt.figure()
      fig, axes = plt.subplots(nrows=2, ncols=1, sharex=False, sharey=False)
      ax = axes.flat[0]
      f = ax.contourf(xs, height, pcp[i,:,:], levels = levels)
      if height.max() > 20000:
          ax.ylim(0,17000)
      if height.max() < 50:
          ax.ylim(0,17)
      cax,kw = mpl.colorbar.make_axes([ax])
      cbar = plt.colorbar(f, cax=cax,**kw)
      plt.suptitle('Max Condensate '+str(i*5) + ' min', size = 20)
      ax = axes.flat[1]
      f2 = ax.plot(np.arange(i)*5,maxw[0:i], linewidth = 2)
      ax.ylim(0,np.max(maxw))
      ax.xlim(0,numfiles*5)
      plt.savefig('../plots/maxcondandmaxw'+xdir+outi+'.png')
      plt.close()

    os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/maxcondandmaxw"+xdir+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/maxcondandmaxw"+xdir+".mp4")
    #os.system("rm ../plots/maxcond"+case+"*.png")



