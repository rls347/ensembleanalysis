import numpy as np
import h5py as hdf
from rachelutils.hdfload import getvar,getrho
from rachelutils.dumbnaming import pert75
import glob

def argheight(var,height,level):
    k = np.argmin(np.abs(height-level))
    varout = var[k,:,:]
    return varout

def findheight(refprof,height,thresh):
    k=0
    if np.max(refprof) > thresh:
        for z in range(len(height)-2):
            if refprof[z] > thresh:
                k=z
    zover10 = refprof[k]
    zunder10 = refprof[k+1]
    hover10 = height[k]
    hunder10 = height[k+1]
    slope = (zunder10 - zover10)/(hunder10 - hover10)
    if slope == 0:
        profheight10 = hover10
    else:
        diffz = (thresh - zover10)/slope
        profheight10 = hover10 + diffz
    return profheight10

def varatheight(prof,height,heightval):
    k = np.argmax(height[np.where(height<heightval)])
    over10 = prof[k]
    under10 = prof[k+1]
    hover10 = height[k]
    hunder10 = height[k+1]
    diffz = heightval-hover10
    slope = (under10 - over10)/(hunder10 - hover10)
    varout = over10 + (slope*diffz)
    return varout

def getheights(ref,height,thresh):
    h10 = np.zeros((33,33))
    maxref = np.max(ref,0)
    for i in range(33):
        for j in range(33):
            if maxref[i,j] > thresh:
                h10[i,j] = findheight(ref[:,i,j],height,thresh)
    return h10

def getvars(var, height, vals):
    w10 = np.zeros((33,33))
    for i in range(33):
        for j in range(33):
            w10[i,j] = varatheight(var[:,i,j],height,vals[i,j])
    return w10


modeldirs = pert75()
times = ['mature','growing']
height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')


for xdir in modeldirs:
    for time in times:
        print xdir, time
        wfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*refbudgetvars*h5'))
        fluxfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*3dfluxes*h5'))
        nt = len(wfiles)
        delzmax=np.zeros((nt-1,33,33))
        wmax=np.zeros((nt-1,33,33))
        dryfluxmax=np.zeros((nt-1,33,33))
        vaporfluxmax=np.zeros((nt-1,33,33))
        netcondfluxmax=np.zeros((nt-1,33,33))

        zdelzmax=np.zeros((nt-1,33,33))
        zwmax=np.zeros((nt-1,33,33))
        zdryfluxmax=np.zeros((nt-1,33,33))
        zvaporfluxmax=np.zeros((nt-1,33,33))
        znetcondfluxmax=np.zeros((nt-1,33,33))

        for t in range(nt-1):
            print t
            w = getvar(wfiles[t],'w')
            ref = getvar(wfiles[t],'ref')
            delz = getvar(wfiles[t+1],'ref')-ref
            dryflux = getvar(fluxfiles[t],'dryflux')
            vaporflux = getvar(fluxfiles[t],'vaporflux')
            netcondflux = getvar(fluxfiles[t],'netcondflux')
            
            delzmax[t,:,:] = np.max(delz,0)
            wmax[t,:,:] = np.max(w,0)
            dryfluxmax[t,:,:] = np.max(dryflux,0)
            vaporfluxmax[t,:,:] = np.max(vaporflux,0)
            netcondfluxmax[t,:,:] = np.max(netcondflux,0)

            zdelzmax[t,:,:] = height[np.argmax(delz,0)]
            zwmax[t,:,:] = height[np.argmax(w,0)]
            zdryfluxmax[t,:,:] = height[np.argmax(dryflux,0)]
            zvaporfluxmax[t,:,:] = height[np.argmax(vaporflux,0)]
            znetcondfluxmax[t,:,:] = height[np.argmax(netcondflux,0)]


        outfilename = time+'-'+xdir+'-2dvars-smoothed3km.h5'
        hf = hdf.File(outfilename,'a')

        hf.create_dataset('valdelzmax',data=delzmax)
        hf.create_dataset('valwmax',data=wmax)
        hf.create_dataset('valdryfluxmax',data=dryfluxmax)
        hf.create_dataset('valvaporfluxmax',data=vaporfluxmax)
        hf.create_dataset('valnetcondfluxmax',data=netcondfluxmax)

        hf.create_dataset('heightdelzmax',data=zdelzmax)
        hf.create_dataset('heightwmax',data=zwmax)
        hf.create_dataset('heightdryfluxmax',data=zdryfluxmax)
        hf.create_dataset('heightvaporfluxmax',data=zvaporfluxmax)
        hf.create_dataset('heightnetcondfluxmax',data=znetcondfluxmax)
        hf.close()





