import numpy as np
import h5py as hdf
import glob
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import case25
from rachelutils.hdfload import getvar

cases = case25()

names = ['Aug 11','Aug 17','Feb 23']
nameout = ['aug11','aug17','feb23']

for c, case in enumerate(cases):
  pcpmax = []
  pcp = {}
  modeldirs = cases[c]
  
  for xdir in modeldirs:
      print xdir
      filename = '/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-023.h5'
      q = getvar(filename,'total_cond')
      meanq=np.mean(q,1)
      meanq[meanq<0.00035]=np.log(0)
      pcp[xdir] = meanq
      pcpmax.append(np.max(meanq))

  height = getvar(filename,'z_coords')/1000.
  xs = np.arange(400)*(0.25)
            
  maxpcp = np.max(np.array(pcpmax))
  levels=np.linspace(0,maxpcp,20)


  fig = plt.figure()
  z2 = []     
  fig, axes = plt.subplots(nrows=5, ncols=5, sharex=True, sharey=True)
     
  for t,xdir in enumerate(modeldirs):
    try:
      ax = axes.flat[t]
      f = ax.contourf(xs, height, pcp[xdir], levels = levels, cmap=plt.get_cmap('plasma'))
      plt.ylim(0,17)
      plt.yticks([0,5,10,15])
      plt.xticks([0,50,100])
    except:
      print 'time ', t, 'has no value in ', xdir
  cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
  cbar = plt.colorbar(f, cax=cax, format='%.1f',**kw)
  cbar.set_label('g/kg')

  plt.suptitle(names[c]+' Mean Condensate', size = 20)
  plt.savefig('postagestamp'+nameout[c]+'.png')
  plt.close()
  plt.clf()

