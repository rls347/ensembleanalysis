import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75,case25

def coloredplot(modeldirs,var,height,nameout,rh,casename):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((var[xdir],height))
        print var[xdir]
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines1 = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines1)
    fig.colorbar(lines1,label='RH')
    ax.set_xlabel('Tracer Flux (#/m$^2$s)')
    ax.set_ylabel('Height (km)')
    ax.set_title('Average Updraft Tracer Flux')
    ax.set_ylim(0,16)
    ax.set_xlim(-1000000000.0, 7000000000.0)

    ax2 = fig.add_axes([.4,.4,.3,.4])
    lines2 = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=2)
    ax2.add_collection(lines2)
    ax2.set_ylim(5,16)
    ax2.set_xlim(-100000000.0, 800000000.0)

    plt.savefig('/nobackup/rstorer/plots/fluxprof-wholeandzoomed'+casename+'.png')
    plt.close()


dirs = case25()


for i, dirname in enumerate(dirs[0]):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))
    outdir = '/nobackup/rstorer/plots/'

height= getvar(files[0],'z_coords')/1000.
profupdraft = np.load('../filesnpz/revuprofile-flux-updraft-tracer.npz')

allrh = np.load('../filesnpz/rhlow.npz')
rh = np.zeros(25)
for i,xdir in enumerate(dirs[0]):
    rh[i]=allrh[xdir]
coloredplot(dirs[0],profupdraft,height,'updraftflux',rh,'aug11')

rh = np.zeros(25)
for i,xdir in enumerate(dirs[1]):
    rh[i]=allrh[xdir]
coloredplot(dirs[1],profupdraft,height,'updraftflux',rh,'aug17')

rh = np.zeros(25)
for i,xdir in enumerate(dirs[2]):
    rh[i]=allrh[xdir]
coloredplot(dirs[2],profupdraft,height,'updraftflux',rh,'feb23')


