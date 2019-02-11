import matplotlib 
matplotlib.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import glob
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

modeldirs = pert75()


cape = np.load('../filesnpz/cape_ML.npz')
rh = np.load('../filesnpz/rhlow.npz')

files = sorted(glob.glob('/nobackup/rstorer/filesnpz/*npz'))
for filename in files:
    variable = np.load(filename)
    print filename
    test = len(variable['feb23-control'].shape)

    varname = filename[27:-4]
    print varname
    if test ==1 :

        outrh = np.zeros(75)
        nt = len(variable['feb23-control'])
        xs = np.arange(nt)*5
        lines = []


        for i,xdir in enumerate(modeldirs):
            outrh[i]=rh[xdir]
            lines.append((xs,variable[xdir]))


        lines = [zip(x,y) for x, y in lines]
        fig, ax = plt.subplots()
        lines = LineCollection(lines, array = outrh, cmap = plt.cm.rainbow, linewidth=3)
        ax.add_collection(lines)
        fig.colorbar(lines)
        ax.autoscale()
        plt.savefig('/nobackup/rstorer/plots/'+varname+'-timeseries-sortedbyrhlow.png')
        plt.close()





