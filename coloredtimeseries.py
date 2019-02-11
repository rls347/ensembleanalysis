import matplotlib 
matplotlib.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import glob
from mpl_toolkits import mplot3d
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
        outmean[x] = np.mean(v)
    return outmax, outmean

modeldirs = pert75()
allcape = np.load('../filesnpz/cape_ML.npz')
allrh = np.load('../filesnpz/rhlow.npz')
rh = np.zeros(75)
cape = np.zeros(75)
for i,xdir in enumerate(modeldirs):
    rh[i]=allrh[xdir]
    cape[i]=allcape[xdir]

names = ['pcprate','w']
for varname in names:
    print varname
    linemax = []
    linemean = []
    outdicmax = {}
    outdicmean = {}

    for i,xdir in enumerate(modeldirs):
        mmx, mmn = gettimeseries(xdir,varname)
        nt = len(mmx)
        print xdir, nt
        xs = np.arange(nt)*5
        linemax.append((xs,mmx))
        linemean.append((xs,mmn))
        outdicmax[xdir]=mmx
        outdicmean[xdir]=mmn
    np.savez('../filesnpz/revu-timeseries-max-'+varname+'.npz',**outdicmax)
    np.savez('../filesnpz/revu-timeseries-mean-'+varname+'.npz',**outdicmean)

    lines = [zip(x,y) for x, y in linemax]

    fig, ax = plt.subplots()
    lines = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines)
    fig.colorbar(lines)
    ax.autoscale()
    plt.savefig('/nobackup/rstorer/plots/'+varname+'-max-timeseries-sortedbyrhlow.png')
    plt.close()

    lines = [zip(x,y) for x, y in linemean]
        
    fig, ax = plt.subplots()
    lines = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines)
    fig.colorbar(lines)
    ax.autoscale()
    plt.savefig('/nobackup/rstorer/plots/'+varname+'-mean-timeseries-sortedbyrhlow.png')
    plt.close()
                                                        
