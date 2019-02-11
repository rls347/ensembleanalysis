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

height = getvar('/nobackup/rstorer/convperts/growing/feb23-control/feb23-control-growing-001.h5','z_coords')
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
        files = sorted(glob.glob('/nobackup/rstorer/convperts/growing/'+xdir+'/*h5'))
        reffiles = sorted(glob.glob('/nobackup/rstorer/convperts/growing/quickbeam/'+xdir+'*h5'))
        rho = getrho(files[0])[:,0,0]
        nt = len(files)
        h10[xdir] = np.zeros((nt,400,400))
        flux10[xdir] = np.zeros((nt,400,400))
        w10[xdir] = np.zeros((nt,400,400))
        maxw[xdir] = np.zeros((nt,400,400))
        for t in range(nt):
            print t
            fil = files[t]
            w = getvar(fil,'w')
            ref = getvar(reffiles[t],'reflectivity')
            cond = getvar(fil,'total_cond')/1000.
            pcp = getvar(fil,'precip3d')
            flux = (cond*w*rho[:,None,None])-pcp
            maxflux = np.max(flux,0)
            maxref = np.max(ref,0)
            maxw[xdir][t,:,:] = np.max(w,0)
            for i in range(400):
                for j in range(400):
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

#        movie(hall, 'growing-movieof'+str(thresh)+'dBheight-fullres-', xdir, height)    
#        movie(diffall,'growing-movieof'+str(thresh)+'dBheightdiff-fullres-',xdir, height) 
#        movie(wall,'growing-movieof'+str(thresh)+'dBheightw-fullres',xdir,height)
#        movie(fluxall,'growing-movieof'+str(thresh)+'dBheightmaxflux-fullres',xdir,height)

        plt.scatter(wall.flatten(),diffall.flatten())
        plt.xlabel('w at '+str(thresh)+' dBZ height')
        plt.ylabel('change in height in 30s')
        plt.savefig('growing-w-h'+str(thresh)+'diff-'+xdir+'-fullres.png')
        plt.clf()

        plt.scatter(maxwall.flatten(),diffall.flatten())
        plt.ylabel('change in height in 30s')
        plt.xlabel('max w in column')
        plt.savefig('growing-maxw-h'+str(thresh)+'diff-'+xdir+'-fullres.png')
        plt.clf()

        plt.scatter(fluxall.flatten(),diffall.flatten())
        plt.ylabel('change in height in 30s')
        plt.xlabel('max net vertical flux in column')
        plt.savefig('growing-maxflux-h'+str(thresh)+'diff-'+xdir+'-fullres.png')
        plt.clf()

    finalw = np.asarray(finalw)
    finalmaxw = np.asarray(finalmaxw)
    finaldiff = np.asarray(finaldiff)
    finalflux = np.asarray(finalflux)

    plt.scatter(finalw.flatten(),finaldiff.flatten())
    plt.xlabel('w at '+str(thresh)+' dBZ height')
    plt.ylabel('change in height in 30s')
    plt.savefig('growing-w-h'+str(thresh)+'diff-controlruns-fullres.png')
    plt.clf()

    plt.scatter(finalmaxw.flatten(),finaldiff.flatten())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max w in column')
    plt.savefig('growing-maxw-h'+str(thresh)+'diff-controlruns-fullres.png')
    plt.clf()

    plt.scatter(finalflux.flatten(),finaldiff.flatten())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max net vertical flux in column')
    plt.savefig('growing-maxflux-h'+str(thresh)+'diff-controlruns-fullres.png')
    plt.clf()




    plt.hist2d(finalw.flatten(),finaldiff.flatten(),bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
    plt.xlabel('w at '+str(thresh)+' dBZ height')
    plt.ylabel('change in height in 30s')
    plt.savefig('growing-w-h'+str(thresh)+'diff-controlruns-fullres-hist2d.png')
    plt.clf()

    plt.hist2d(finalmaxw.flatten(),finaldiff.flatten(),bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max w in column')
    plt.savefig('growing-maxw-h'+str(thresh)+'diff-controlruns-fullres-hist2d.png')
    plt.clf()

    plt.hist2d(finalflux.flatten(),finaldiff.flatten(),bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
    plt.ylabel('change in height in 30s')
    plt.xlabel('max net vertical flux in column')
    plt.savefig('growing-maxflux-h'+str(thresh)+'diff-controlruns-fullres-hist2d.png')
    plt.clf()




