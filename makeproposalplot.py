import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import ticker

import numpy as np
from rachelutils.genericplots import movie
from rachelutils.hdfload import getvar
import glob

files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/quickbeam/cloudsat/feb23-control*h5'))
ref = []
for fil in files:
    r = getvar(fil,'reflectivity')

    #ref.append(np.mean(r[:,190:195,:],1))
#fil = files[35]
#r = getvar(fil,'reflectivity')
    for f in range(150,220,5):
        ref.append(np.mean(r[:,f:f+5,:],1))


height =getvar( '/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')

movie(ref,'/nobackup/rstorer/plots/moviereflectivityslice','feb23-control',height)
height = height/1000

refcontrol = getvar('/nobackup/rstorer/convperts/revu/quickbeam/cloudsat/feb23-pert9-revu-036-quickbeam-cloudsat.h5','reflectivity')
slicecontrol = np.mean(refcontrol[:,190:195,:],1)

wcontrol = getvar('/nobackup/rstorer/convperts/revu/feb23-pert9/feb23-pert9-revu-036.h5','w')
slicecontrolw = wcontrol[:,192,:]# np.mean(wcontrol[:,190:195,:],1)
slicecontrolw[slicecontrolw <1]=0

refpert9 = getvar('/nobackup/rstorer/convperts/revu/quickbeam/cloudsat/feb23-pert9-revu-036-quickbeam-cloudsat.h5','reflectivity')
slicepert9 = np.mean(refpert9[:,220:225,:],1)

wpert9 = getvar('/nobackup/rstorer/convperts/revu/feb23-pert9/feb23-pert9-revu-036.h5','w')
slicepert9w = wpert9[:,222,:]#np.mean(wpert9[:,220:225,:],1)
slicepert9w[slicepert9w<1]=0

xs = np.arange(400)*.25

plt.subplot(2,1,1)
plt.contourf(xs[::4],height,slicecontrol[:,::4],levels=np.linspace(-40,20,20))
#plt.contour(xs,height,slicecontrolw,levels = [.1])
plt.ylim(0,18)
plt.xlim(0,80)
plt.ylabel('km')
cbar = plt.colorbar(label = 'dBZ')
tick_locator = ticker.MaxNLocator(nbins=7)
cbar.locator = tick_locator
cbar.update_ticks()
cbar.ax.set_yticklabels([-40,-30,-20,-10,0,10,20])
plt.subplot(2,1,2)
plt.contourf(xs[::4],height,slicepert9[:,::4],levels=np.linspace(-40,20,20))
#plt.contour(xs,height,slicepert9w,levels = [.1])
plt.ylim(0,18)
plt.xlim(0,80)
plt.ylabel('km')
plt.xlabel('km')
cbar =plt.colorbar(label='dBZ')
tick_locator = ticker.MaxNLocator(nbins=7)
cbar.locator = tick_locator
cbar.update_ticks()
cbar.ax.set_yticklabels([-40,-30,-20,-10,0,10,20])

plt.savefig('compare2sims.png')
plt.clf()
