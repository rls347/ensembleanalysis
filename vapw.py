import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

def smoothedvar(var):
    smoothvar = np.zeros((82,33,33))-40
    var[var<-40] = -40
    for h in range(82):
        for i in range(9,402,12):
            iind = (i-9)/12
            for j in range(9,402,12):
                jind = (j-9)/12
                smoothvar[h,iind,jind] = np.mean(var[h,i-6:i+6,j-6:j+6])
    return smoothvar

def getmax(var, z):
    height5km = np.argmin(np.abs(z-5000))
    maxvar = np.max(var[height5km:,:,:],0)
    return maxvar

dirs = pert75()
#dirs = ['aug17-control','feb23-control','aug11-control']

times = ['mature','growing']
for time in times:
    outw = {}
    outdel = {}
    for xdir in dirs:
        print xdir
        modelfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/'+xdir+'/*h5'))
        radarfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/quickbeam/'+xdir+'*h5'))
        height = getvar(modelfiles[0],'z_coords')
        nt = len(modelfiles)
        outwlist=[]
        outdellist=[]
        for t in range(nt-3):
            print t
            w = smoothedvar(getvar(modelfiles[t],'w'))
            z1 = smoothedvar(getvar(radarfiles[t],'reflectivity'))
            z2 = smoothedvar(getvar(radarfiles[t+3],'reflectivity'))
            diff = (z2-z1)/1.5

            ws = getmax(w, height)
            dels = getmax(diff, height)

            outdellist.extend(dels[ws>=1])
            outwlist.extend(ws[ws>=1])

        outw[xdir]=np.asarray(outwlist)
        outdel[xdir]=np.asarray(outdellist)
        if len(outw[xdir]) > 2:
            plt.scatter(outw[xdir],outdel[xdir])

    np.savez(time+'maxw-3kmavg-take2.npz',**outw)
    np.savez(time+'maxdelz-3kmavg-take2.npz',**outdel)
    plt.title('3km Footprint, 90s Separation')
    plt.xlabel('Max W (m/s)')
    plt.ylabel('Max dZ/dt (dBZ/min)')
    plt.savefig(time+'firstscattertest-take2.png')




