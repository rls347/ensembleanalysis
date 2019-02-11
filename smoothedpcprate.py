import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

def smoothedvar(var):
    smoothvar = np.zeros((33,33))-40
    var[var<-40] = -40
    for i in range(6,402,12):
        iind = (i-6)/12
        for j in range(6,402,12):
            jind = (j-6)/12
            smoothvar[iind,jind] = np.mean(var[i-6:i+6,j-6:j+6])
    return smoothvar

dirs = pert75()
#dirs = ['aug11-control','feb23-control','aug17-control']

times = ['mature','growing','revu']
for time in times:
    for xdir in dirs:
        print xdir
        modelfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/'+xdir+'/*h5'))
        nt = len(modelfiles)
        for t in range(nt):
            print t
            q = smoothedvar(getvar(modelfiles[t],'pcprate'))
            tout = str(t)
            if t<10:
                tout = '0'+tout

            outfilename = time+'-'+xdir+'-pcprate-smoothed3km-'+tout+'.h5'
            hf = hdf.File(outfilename,'w')
            hf.create_dataset('q',data=q)
            hf.close()


