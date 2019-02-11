import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

def makeplots(fil1,dt,num):
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    w = getvar(fil1,'w')
    colmax = np.max(w,0)
    w1 = np.where(colmax>5)

    wup= w[:,w1[0],w1[1]]

    wout= np.mean(wup,1)

    return wout

dirs = pert75()
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')

#allw= {}
for i, dirname in enumerate(dirs):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))
    outdir = '/nobackup/rstorer/plots/'

#    intup= np.zeros(82)
#    intnum = 0.
#
#    for num in range(1,len(files)-1):
#        up = makeplots(files[num],300.,num)
#        if np.max(up) > 0:
#            intup = intup + up
#            intnum +=1
#    intup = intup / intnum
#
#    allw[dirname] = intup

#np.savez('../filesnpz/revuprofile-flux-w.npz',**allw)

allw = np.load('../filesnpz/revuprofile-flux-updraft-tracer.npz')

height = getvar(files[0], 'z_coords')/1000.
for i, dirname in enumerate(dirs):
    intup = allw[dirname] 
    if i ==0:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
plt.legend()
plt.ylim([0,20])
plt.ylabel('km')
plt.xlabel('m/s')
plt.title('Time Average Updraft Profiles')
plt.savefig(outdir+'/fluxprofs-revu-maxwgt5-allruns-tracer2.png')
plt.clf()




