import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar, getrho
import glob
from rachelutils.genericplots import movie
from rachelutils.dumbnaming import pert75


def findheight(refprof,wprof,fluxprof,height,thresh):
    k=0
    if np.max(refprof) > thresh:
        for z in range(len(height)-2):
            if refprof[z] > thresh:
                k=z
    zover10 = refprof[k]
    zunder10 = refprof[k+1]
    hover10 = height[k]
    hunder10 = height[k+1]
    wover10 = wprof[k]
    wunder10 = wprof[k+1]
    fover10 = fluxprof[k]
    funder10 = fluxprof[k+1]
    slope = (zunder10 - zover10)/(hunder10 - hover10)
    if slope == 0:
        print 'hmm'
        profheight10 = hover10
        profw10 = wover10
        profflux10 = fover10
    else:
        diffz = (thresh - zover10)/slope
        profheight10 = hover10 + diffz
        wslope = (wunder10 - wover10)/(hunder10 - hover10)
        profw10 = wover10 + (wslope * diffz)
        fslope = (funder10 - fover10)/(hunder10 - hover10)
        profflux10 = fover10 + (fslope*diffz)
    if np.abs(profw10) > 50:
        print profw10,slope, diffz, wslope,zover10,zunder10
        print refprof
    return profheight10,profw10,profflux10

modeldirs = pert75()
modeldirs = ['feb23-control','aug11-control','aug17-control']

height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')
km5 = np.argmin(np.abs(height-5000))
km8 = np.argmin(np.abs(height-8000))

h10 = np.load('mature-h10.npz')
w10 = np.load('mature-w10.npz')
flux10 = np.load('mature-flux10.npz')

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/'+xdir+'/*h5'))
    reffiles = sorted(glob.glob('/nobackup/rstorer/convperts/mature/quickbeam/'+xdir+'*h5'))
    nt = len(files)
    allh = h10[xdir]
    allw = w10[xdir]
    allflux = flux10[xdir]

#    w1 = getvar(files[0],'w')[km8,:,:]
#    core = np.where(w>1)
#    xmin,xmax = (np.min(np.asarray(core[0])),np.max(np.asarray(core[0])))
#    ymin,ymax = (np.min(np.asarray(core[1])),np.max(np.asarray(core[1])))

    
#    for t in range(nt):
#        print t
#        fil = files[t]
#        w = getvar(fil,'w')[km8,:,:]
#        core = np.where(w>1)
#        usew.extend(allw[t,core[0][:],core[1][:]])
#        useh.extend(allh[t,core[0][:],core[1][:]])
#        useflux.extend(allflux[t,core[0][:],core[1][:]])
    print allh.max(), allh.min(), allh.shape    
    movie(allh, 'movieof10dBheight-', xdir, height)



