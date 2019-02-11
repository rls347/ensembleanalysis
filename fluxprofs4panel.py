import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

dirs = pert75()
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')

for i, dirname in enumerate(dirs):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))

#allflux = np.load('revuprofile-flux-netvertical.npz')
#allprecip = np.load('revuprofile-flux-precip.npz')
#allupdraft = np.load('revuprofile-flux-updraft.npz')


allflux = np.load('revuprofile-flux-netvertical-gt2.npz')
allprecip = np.load('revuprofile-flux-precip-gt2.npz')
allupdraft = np.load('revuprofile-flux-updraft-gt2.npz')


height = getvar(files[0], 'z_coords')/1000.

allrh = np.load('rhlow.npz')
rh = np.zeros(75)
for i,xdir in enumerate(dirs):
    rh[i]=allrh[xdir]

fig,axes = plt.subplots(nrows=2,ncols=2)

ax = axes[0,0]
for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] 
    if i ==0:
        ax.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Feb 23')
    else:
        ax.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i])
#plt.legend()
ax.set_ylim([0,20])
ax.set_ylabel('km')
ax.set_xticks(ax.get_xticks()[::2])
ax.set_title('Updraft Mass Flux')

ax1 = axes[0,1]
for i, dirname in enumerate(dirs):
    intup = allprecip[dirname]
    if i ==0:
        ax1.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax1.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax1.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Feb 23')
    else:
        ax1.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i])
ax1.legend(bbox_to_anchor=[1.6,.8],prop={'size': 12})
ax1.set_ylim([0,20])
ax1.set_yticks([])
ax1.set_xticks(ax1.get_xticks()[::2])
ax1.set_title('Precipitation Flux') 

ax2 = axes[1,0]
for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allprecip[dirname]
    if i ==0:
        ax2.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax2.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax2.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i], label = 'Feb 23')
    else:
        ax2.plot(intup[1:],height[1:], linewidth=2, alpha=.7, color = cols[i])
ax2.set_ylim([0,20])
ax2.set_ylabel('km')
ax2.set_xticks([-0.006,0.00,0.006])
ax2.set_xlabel('kg/m$^2$s')
ax2.set_title('Net Flux')

plotvars=[]
ax3 = axes[1,1]
for i,dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allprecip[dirname]
    plotvars.append((intup,height))
    lines = [zip(x,y) for x, y in plotvars]
lines = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=2,alpha=.7)
ax3.add_collection(lines)
ax3.set_xticks(ax2.get_xticks())
ax3.set_yticks([])
ax3.set_title('Net Flux')
ax3.set_xlabel('kg/m$^2$s')
#ax3.add_colorbar(lines)
ax3.set_ylim(0,20)
ax3.set_xlim(ax2.get_xlim())
plt.tight_layout()

fig.subplots_adjust(right = .8)
ax5 = fig.add_axes([.84,.14,.03,.3],frameon=False, xticks=[], yticks=[])
fig.colorbar(lines, cax=ax5,label = 'RH')



plt.savefig('flux4panel-2ms.png')
