import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def makesum(varin):
    varout = {}
    for nam in varin.keys():
        x = varin[nam]
        x[np.isnan(x)]=0.
#        x = x*300
        y=np.cumsum(x)
        varout[nam]=y
    return varout

def coloredplot(modeldirs,var,height,nameout,rh):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((height[xdir],var[xdir]))
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines)
    fig.colorbar(lines)
    ax.autoscale()
    plt.savefig('/nobackup/rstorer/code/timeseriesflux-'+nameout+'-sortedbyrhlow-summed-8km-vapor-onlyw.png')
    plt.close()

def getbudgetvars(fil1,dt):
    print fil1
    w = getvar(fil1, 'w')
    return w

def makeplots(fil1,dt,num):
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    w= getbudgetvars(fil1,dt)
    colmax = np.max(w,0)
    w1 = np.where(colmax>5)

    updraft = w[:,w1[0],w1[1]]

    up = np.mean(updraft,1)

    return up

dirs = pert75()
#dirs = ['feb23-control']
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')

allupdraft = {}
for i, dirname in enumerate(dirs):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/'+dirname+'*h5'))
    outdir = '/nobackup/rstorer/code/'
    nt = len(files)

    intup= np.zeros(nt)
    intnum = 0.

    z = getvar(files[0],'z_coords')
    zarg = np.argmin(np.abs(z-8000))

    for num in range(1,nt-1):
        up= makeplots(files[num],300.,num)
        intup[num] = up[zarg]

    allupdraft[dirname] = intup



height = {}
allrh = np.load('../filesnpz/rhlow.npz')
#allrh = np.load('../filesnpz/totpcpmm.npz')
rh = np.zeros(75)
for i,xdir in enumerate(dirs):
    rh[i]=allrh[xdir]
    height[xdir] = np.arange(len(allupdraft[xdir])) *5

coloredplot(dirs,allupdraft,height,'updraftflux',rh)

for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] 
    if i ==0:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i])
plt.legend()
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Updraft Profiles')
plt.savefig(outdir+'/fluxtime-revu-maxwgt5-allruns-updraft-summed-8km-vapor-onlyw.png')
plt.clf()


up = np.zeros(75)
for i,dirname in enumerate(dirs):
    up[i]=allupdraft[dirname][-1]


plt.scatter(rh,up)
p = np.poly1d(np.polyfit(rh,up,2))
variance = np.var(up)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,up)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/fluxscatter-revu-maxwgt5-allruns-updraft-summed-8km-vapor-onlyw.png')
plt.clf()


