import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

def smoothedvar(var):
#    smoothvar = np.zeros((45,33,33))-40
    smoothvar = np.zeros((82,33,33))-40
    var[var<-40] = -40
    for h in range(82):
        hind = h#+37
        for i in range(6,402,12):
            iind = (i-6)/12
            for j in range(6,402,12):
                jind = (j-6)/12
                smoothvar[h,iind,jind] = np.mean(var[hind,i-6:i+6,j-6:j+6])
    return smoothvar

dirs = pert75()
#dirs = ['aug11-control','feb23-control','aug17-control']

times = ['mature','growing','revu']
times = ['mature']
for time in times:
    for xdir in dirs:
        print xdir
        modelfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/'+xdir+'/*h5'))
        height = getvar(modelfiles[0],'z_coords')[37:]
        dz = getdz(modelfiles[0])[37:]
        nt = len(modelfiles)
        for t in range(nt):
            print t
            q = smoothedvar(getvar(modelfiles[t],'vapor'))
            tout = str(t)
            if t<10:
                tout = '0'+tout

            outfilename = time+'-'+xdir+'-vapor-smoothed3km-'+tout+'.h5'
            hf = hdf.File(outfilename,'w')
            hf.create_dataset('q',data=q)
            hf.close()


