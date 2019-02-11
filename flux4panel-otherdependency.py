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

allflux = np.load('../filesnpz/revuprofile-flux-netvertical.npz')
allprecip = np.load('../filesnpz/revuprofile-flux-precip.npz')
allupdraft = np.load('../filesnpz/revuprofile-flux-updraft.npz')

height = getvar(files[0], 'z_coords')/1000.

allshear = np.load('../filesnpz/shear.npz')
shear = np.zeros(75)
for i,xdir in enumerate(dirs):
    shear[i]=allshear[xdir]

fig,axes = plt.subplots(nrows=3,ncols=2)

ax = axes[0,0]
for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] 
    if i ==0:
        ax.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        ax.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
#plt.legend()
ax.set_ylim([0,20])
ax.set_ylabel('km')
ax.set_xticks(ax.get_xticks()[::2])
ax.set_title('Updraft Mass Flux')

ax1 = axes[1,0]
for i, dirname in enumerate(dirs):
    intup = allprecip[dirname]
    if i ==0:
        ax1.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax1.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax1.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        ax1.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
ax1.legend(bbox_to_anchor=[2.8,1],prop={'size': 12})
ax1.set_ylim([0,20])
#ax1.set_yticks([])
ax1.set_xticks(ax1.get_xticks()[::2])
ax1.set_title('Precipitation Flux') 

ax2 = axes[2,0]
for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allprecip[dirname]
    if i ==0:
        ax2.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        ax2.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        ax2.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        ax2.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
ax2.set_ylim([0,20])
ax2.set_ylabel('km')
ax2.set_xticks([-0.006,0.00,0.006])
ax2.set_xlabel('kg/m$^2$s')
ax2.set_title('Net Flux')

plotvars = []
ax4 = axes[0,1]
for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname]
    plotvars.append((intup,height))                 
lines1 = [zip(x,y) for x, y in plotvars]         
lines1 = LineCollection(lines1, array = shear, cmap = plt.cm.rainbow, linewidth=3)
ax4.add_collection(lines1)

ax4.set_ylim([0,20])
ax4.set_xlim(ax.get_xlim())
#ax.set_ylabel('km')
ax4.set_xticks(ax4.get_xticks()[::2])
ax4.set_title('Updraft Mass Flux')

ax7 = axes[1,1]
for i, dirname in enumerate(dirs):
    intup = allprecip[dirname]
    plotvars.append((intup,height))                 
    lines2 = [zip(x,y) for x, y in plotvars]         
lines2 = LineCollection(lines2, array = shear, cmap = plt.cm.rainbow, linewidth=3)
ax7.add_collection(lines2)
#ax7.legend(bbox_to_anchor=[1.6,.8],prop={'size': 12})
ax7.set_ylim([0,20])
ax7.set_xlim(ax1.get_xlim())
#ax1.set_yticks([])
ax7.set_xticks(ax7.get_xticks()[::2])
ax7.set_title('Precipitation Flux')

plotvars=[]
ax3 = axes[2,1]
for i,dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allprecip[dirname]
    plotvars.append((intup,height))
lines3 = [zip(x,y) for x, y in plotvars]
lines3 = LineCollection(lines3, array = shear, cmap = plt.cm.rainbow, linewidth=3)
ax3.add_collection(lines3)
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
fig.colorbar(lines3, cax=ax5,label = 'shear')



plt.savefig('../plots/flux4panel-byshear.png')
