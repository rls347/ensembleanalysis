import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import glob
from scipy.interpolate import spline



def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)


modeldirs = pert75()

frzlapse = {}
botlapse = {}

for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'*h5'))
    t = getvar(files[0],'tempk')[:,0,0]
    z = getvar(files[0],'z_coords')/1000.

    lapse = np.zeros(len(t)-1)
    zplot = np.zeros(len(t)-1)

    for x in range(len(lapse)):
        lapse[x] = (t[x+1]-t[x])/(z[x+1]-z[x])
        zplot[x] = (z[x+1]+z[x])/2.

    spl = running_mean(lapse,5)

    plt.plot(spl,zplot[:-4],linewidth=3)
    plt.xlabel('Lapse Rate (K/km)')
    plt.ylim(0,18)
    plt.ylabel('Height')
    plt.title(xdir)
    plt.savefig('lapserate2z-'+xdir+'.png')
    plt.clf()

    print z[np.argmin(np.abs(t-273.15))]

    layerfreez = np.logical_and(z>4.0, z<6.0)
    layerbot = np.logical_and(z>0.0, z<4.0)

    frzlapse[xdir] = np.max(lapse[layerfreez])
    botlapse[xdir] = np.max(lapse[layerbot])

np.savez('lapserate2z_freezing4-6.npz',**frzlapse)
np.savez('lapserate2z_below4.npz',**botlapse)



print frzlapse
print ''
print botlapse
