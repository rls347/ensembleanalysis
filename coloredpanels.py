import matplotlib as mpl
mpl.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import case25, pert75
import glob
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def gettimeseries(xdir,varname):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nt = len(files)
    outmax = np.zeros(nt)
    outmean = np.zeros(nt)
    for x,fil in enumerate(files):
        v = getvar(fil,varname)
        outmax[x] = np.max(v)
        outmean[x] = np.mean(v[v>1])
    return outmax, outmean

allmodeldirs = case25()
allrh = np.load('../filesnpz/rhlow.npz')
pert75 = pert75()
rh = np.zeros(75)
allvar = np.load('../filesnpz/revu-timeseries-mean-pcprate.npz')
wvar = np.load('../filesnpz/revu-timeseries-max-w.npz')
lls=[]
for i,xdir in enumerate(pert75):
    rh[i] = allrh[xdir]
    mmx = allvar[xdir]
    nt = len(mmx)
    xs = np.arange(nt)*5
    lls.append((xs,mmx))
ll= [zip(x,y) for x,y in lls]
ll = LineCollection(ll, array = rh, cmap = plt.cm.plasma)
fig, ax = plt.subplots()
ax.add_collection(ll)
plt.savefig('vartest.png')
plt.close()
c = ll.get_color()
varname = 'pcprate'

fig, ax = plt.subplots(nrows=3,ncols=2)
contoursets = []

for case in range(3):
    modeldirs = allmodeldirs[case]
    linemax = []
    linew = []
    for i,xdir in enumerate(modeldirs):
        mmx = allvar[xdir]
        w = wvar[xdir]
        nt = len(mmx)
        xs = np.arange(nt)*5
        linemax.append((xs,mmx))
        linew.append((xs,w))

    linest = [zip(x,y) for x, y in linemax]

    axq = ax[case,0]
    lines = LineCollection(linest,colors=c[case*25:case*25+25], cmap = plt.cm.plasma, linewidth=2, alpha=.7)
    contoursets.append(lines)
    axq.add_collection(lines)
    axq.autoscale()
    axq.set_ylabel('mm/hr')

    ww = [zip(x,y) for x, y in linew]
    axn = ax[case,1]
    lines2 = LineCollection(ww, colors = c[case*25:case*25+25], cmap = plt.cm.plasma, linewidth=2, alpha=.7)
    contoursets.append(lines2)
    axn.add_collection(lines2)
    axn.autoscale()
    axn.yaxis.tick_right()
    axn.yaxis.set_label_position("right")
    axn.set_ylabel('m/s')

    if case ==0:
        axq.set_title('Mean Rain Rate',fontsize=14, fontweight = 'bold')
        axn.set_title('Max Vertical Velocity',fontsize=14, fontweight = 'bold')

    if case ==2:
        axq.set_xlabel('Minutes')
        axn.set_xlabel('Minutes')
plt.tight_layout()
fig.subplots_adjust(bottom=.25)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#fig.colorbar(im, cax=cbar_ax)
    
#cax,kw = mpl.colorbar.make_axes([aax for aax in ax.flat])
#plt.colorbar(contoursets[0],cax,**kw)

cmap = plt.cm.plasma
norm = mpl.colors.Normalize(vmin = rh.min(), vmax = rh.max())
ax3 = fig.add_axes([0.3, 0.1, 0.4, 0.03])
cb1 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap,norm=norm,orientation='horizontal')
cb1.set_label('Low Level RH')

fig.subplots_adjust(left = .2)
ax4 = fig.add_axes([.04,0.77,0.05,0.05],frameon=False, xticks=[], yticks=[])
ax4.set_title('Aug 11',fontweight='bold')
ax5 = fig.add_axes([.04,.52,.05,.05],frameon=False, xticks=[], yticks=[])
ax5.set_title('Aug 17',fontweight='bold')
ax6 = fig.add_axes([.04,.27,.05,.05],frameon=False, xticks=[], yticks=[])
ax6.set_title('Feb 23',fontweight='bold')

plt.savefig('variabilitytimeseries.png')
plt.close()





    





