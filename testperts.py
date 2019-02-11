import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import glob
import numpy as np
from rachelutils.hdfload import getvar, meanprof
from rachelutils.dumbnaming import pert75

perts = pert75()

t = {}
rh = {}
tdiff = {}
rhdiff = {}

for p in perts:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+p+'/'+p+'*h5'))
    t[p] = meanprof(files[0],'tempk')
    rh[p] = meanprof(files[0],'relhum')

z = getvar(files[0],'z_coords')

for i in range(1,25):
    tdiff[perts[i]] = t[perts[i]] - t['aug11-control']
    rhdiff[perts[i]] = rh[perts[i]] - rh['aug11-control']

    tdiff[perts[i+25]] = t[perts[i+25]] - t['aug17-control']
    rhdiff[perts[i+25]] = rh[perts[i+25]] - rh['aug17-control']

    tdiff[perts[i+50]] = t[perts[i+50]] - t['feb23-control']
    rhdiff[perts[i+50]] = rh[perts[i+50]] - rh['feb23-control']

    plt.plot(tdiff[perts[i]],z,color='green',linewidth=3,label='aug11')
    plt.plot(tdiff[perts[i+25]],z,color='blue',linewidth=3,label='aug17') 
    plt.plot(tdiff[perts[i+50]],z,color='purple',linewidth=3,label='feb23') 
    plt.legend()
    plt.ylim(0,20000)
    plt.xlim(-1.5,1.5)
    plt.title('Temperature Perturbation ' + str(i))
    plt.savefig('tperts'+str(i)+'.png')
    plt.clf()

    plt.plot(rhdiff[perts[i]],z,color='green',linewidth=3,label='aug11')  
    plt.plot(rhdiff[perts[i+25]],z,color='blue',linewidth=3,label='aug17')
    plt.plot(rhdiff[perts[i+50]],z,color='purple',linewidth=3,label='feb23')
    plt.legend()
    plt.ylim(0,20000)
    plt.xlim(-10,10)
    plt.title('RH Perturbation ' + str(i))
    plt.savefig('rhperts'+str(i)+'.png')
    plt.clf()



