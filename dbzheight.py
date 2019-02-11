import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar, getrho
import glob
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
#modeldirs = ['feb23-control','aug11-control','aug17-control']

height = getvar('/nobackup/rstorer/convperts/growing/feb23-control/feb23-control-growing-001.h5','z_coords')
km5 = np.argmin(np.abs(height-5000))
h10 = {}
w10 = {}
flux10 = {}


#h10 = np.load('growing-controlonly-h10.npz')
#w10 = np.load('growing-controlonly-w10.npz')
#flux10 = np.load('growing-controlonly-flux10.npz')

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/growing/'+xdir+'/*h5'))
    reffiles = sorted(glob.glob('/nobackup/rstorer/convperts/growing/quickbeam/'+xdir+'*h5'))
    nt = len(files)
    h10[xdir] = np.zeros((nt,400,400))
    w10[xdir] = np.zeros((nt,400,400))
    flux10[xdir] = np.zeros((nt,400,400))
    for t in range(nt):
        print t
        fil = files[t]
        flux = ((getvar(fil,'total_cond')[km5:,:,:]/1000.) * getvar(fil,'w')[km5:,:,:] * getrho(fil)[km5:,:,:]) - getvar(fil,'precip3d')[km5:,:,:]
        w = getvar(fil,'w')[km5:,:,:]
        ref = getvar(reffiles[t],'reflectivity')[km5:,:,:]
        ref[ref<-40]=-40
        maxref = np.max(ref,0)
        for i in range(400):
            for j in range(400):
                if maxref[i,j] >10 and np.max(w[:,i,j])>1:
                    h10[xdir][t,i,j],w10[xdir][t,i,j],flux10[xdir][t,i,j] = findheight(ref[:,i,j],w[:,i,j],flux[:,i,j],height[km5:],10.)
    wall = w10[xdir][0:-1,:,:]
    fluxall = flux10[xdir][0:-1,:,:]
    h10all = h10[xdir][0:-1,:,:]
    diffall = np.diff(h10[xdir], axis=0)
    diffall[h10all < 1000] = 0


    plt.scatter(fluxall.flatten(),diffall.flatten())
    plt.savefig('netflux-h10diff-'+xdir+'.png')
    plt.clf()

    plt.scatter(wall.flatten(),diffall.flatten())
    plt.savefig('w-h10diff-'+xdir+'.png')
    plt.clf()

np.savez('growing-h10.npz',**h10)
np.savez('growing-w10.npz',**w10)
np.savez('growing-flux10.npz',**flux10)



