import numpy as np
from rachelutils.genericplots import movie
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
    fluxover10 = fluxprof[k]
    fluxunder10 = fluxprof[k+1]
    slope = (zunder10 - zover10)/(hunder10 - hover10)
    if slope == 0:
        print 'hmm'
        profheight10 = hover10
        profw10 = wover10
        profflux10 = fluxover10
    else:
        diffz = (thresh - zover10)/slope
        profheight10 = hover10 + diffz
        wslope = (wunder10 - wover10)/(hunder10 - hover10)
        profw10 = wover10 + (wslope * diffz)
        fluxslope = (fluxunder10 - fluxover10)/(hunder10 - hover10)
        profflux10 = fluxover10 + (fluxslope * diffz)
    return profheight10,profw10,profflux10

modeldirs = pert75()
modeldirs = ['feb23-control','aug11-control','aug17-control']

height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')
h10 = {}
flux10 = {}
w10 = {}

maxw = {}

vals = [0,5,10,20]

for thresh in vals:

    finalw = []
    finalmaxw = []
    finaldiff = []
    finalflux = []

    for xdir in modeldirs:
        print xdir
        files = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'*refbudgetvars*h5'))
        condfiles = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'*cond*3km*h5'))
        pcpfiles = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'*precip*3km*h5'))
        rho = getrho('/nobackup/rstorer/convperts/mature/'+xdir+'/'+xdir+'-mature-001.h5')[:,0,0]
        nt = len(files)
        print len(files),len(condfiles),len(pcpfiles),nt
        h10[xdir] = np.zeros((nt,33,33))
        flux10[xdir] = np.zeros((nt,33,33))
        w10[xdir] = np.zeros((nt,33,33))
        maxw[xdir] = np.zeros((nt,33,33))
        for t in range(nt):
            print t
            fil = files[t]
            w = getvar(fil,'w')
            ref = getvar(fil,'ref')
            cond = getvar(condfiles[t],'q')/1000.
            pcp = getvar(pcpfiles[t],'q')
            flux = (cond*w*rho[:,None,None])-pcp
            maxflux = np.max(flux,0)
            maxref = np.max(ref,0)
            maxw[xdir][t,:,:] = np.max(w,0)
            for i in range(33):
                for j in range(33):
                    if maxref[i,j] >10:
                        h10[xdir][t,i,j],w10[xdir][t,i,j],flux10[t,i,j] = findheight(ref[:,i,j],w[:,i,j],flux[:,i,j],height,thresh)
            flux10[xdir][t,:,:]=maxflux
        wall = w10[xdir][0:-1,:,:]
        fluxall = flux10[xdir][0:-1,:,:]
        diffall = np.diff(h10[xdir], axis=0)
        maxwall = maxw[xdir][0:-1,:,:]
        hall = h10[xdir][0:-1,:,:]

        hall[diffall<-1000]=0
        hall[diffall>1000]=0
        fluxall[diffall<-1000]=0
        fluxall[diffall>1000]=0
        wall[diffall>1000]=0
        wall[diffall<-1000]=0
        maxwall[diffall<-1000]=0
        maxwall[diffall>1000]=0

        diffall[diffall>1000]=0
        diffall[diffall<-1000]=0
        


        finalw.append(wall)
        finalmaxw.append(maxwall)
        finaldiff.append(diffall)
        finalflux.append(fluxall)

#        movie(hall, 'mature-movieof'+str(thresh)+'dBheight-3km-', xdir, height)    
#        movie(diffall,'mature-movieof'+str(thresh)+'dBheightdiff-3km-',xdir, height) 
#        movie(wall,'mature-movieof'+str(thresh)+'dBheightw-3km',xdir,height)
#        movie(fluxall,'mature-movieof'+str(thresh)+'dBheightmaxflux-3km',xdir,height)

        plt.scatter(wall.flatten(),diffall.flatten())
        plt.xlabel('w at '+str(thresh)+' dBZ height')
        plt.ylabel('change in height in 30s')
        plt.savefig('mature-w-h'+str(thresh)+'diff-'+xdir+'-3km.png')
        plt.clf()

        plt.scatter(maxwall.flatten(),diffall.flatten())
        plt.ylabel('change in height in 30s')
        plt.xlabel('max w in column')
        plt.savefig('mature-maxw-h'+str(thresh)+'diff-'+xdir+'-3km.png')
        plt.clf()

        plt.scatter(fluxall.flatten(),diffall.flatten())
        plt.ylabel('change in height in 30s')
        plt.xlabel('max net vertical flux in column')
        plt.savefig('mature-maxflux-h'+str(thresh)+'diff-'+xdir+'-3km.png')
        plt.clf()

    finalw = np.asarray(finalw)
    finalmaxw = np.asarray(finalmaxw)
    finaldiff = np.asarray(finaldiff)
    finalflux = np.asarray(finalflux)

    plt.scatter(finalw.flatten(),finaldiff.flatten())
    plt.xlabel('w at '+str(thresh)+' dBZ height')
    plt.ylabel('change in height in 30s')
    plt.savefig('mature-w-h'+str(thresh)+'diff-controlruns-3km.png')
    plt.clf()

    plt.scatter(finalmaxw.flatten(),finaldiff.flatten())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max w in column')
    plt.savefig('mature-maxw-h'+str(thresh)+'diff-controlruns-3km.png')
    plt.clf()

    plt.scatter(finalflux.flatten(),finaldiff.flatten())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max net vertical flux in column')
    plt.savefig('mature-maxflux-h'+str(thresh)+'diff-controlruns-3km.png')
    plt.clf()
