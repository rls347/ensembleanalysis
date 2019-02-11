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
        height0db=np.zeros((nt-1,33,33))
        height5db=np.zeros((nt-1,33,33))
        height10db=np.zeros((nt-1,33,33))
        height20db=np.zeros((nt-1,33,33))
        w0db=np.zeros((nt-1,33,33))
        w5db=np.zeros((nt-1,33,33))
        w10db=np.zeros((nt-1,33,33))
        w20db=np.zeros((nt-1,33,33))
        dryflux0db=np.zeros((nt-1,33,33))
        dryflux5db=np.zeros((nt-1,33,33))
        dryflux10db=np.zeros((nt-1,33,33))
        dryflux20db=np.zeros((nt-1,33,33))
        vaporflux0db=np.zeros((nt-1,33,33))
        vaporflux5db=np.zeros((nt-1,33,33))
        vaporflux10db=np.zeros((nt-1,33,33))
        vaporflux20db=np.zeros((nt-1,33,33))
        netcondflux0db=np.zeros((nt-1,33,33))
        netcondflux5db=np.zeros((nt-1,33,33))
        netcondflux10db=np.zeros((nt-1,33,33))
        netcondflux20db=np.zeros((nt-1,33,33))
        delz5km=np.zeros((nt-1,33,33))
        delz8km=np.zeros((nt-1,33,33))
        delz10km=np.zeros((nt-1,33,33))
        w5km=np.zeros((nt-1,33,33))
        w8km=np.zeros((nt-1,33,33))
        w10km=np.zeros((nt-1,33,33))
        dryflux5km=np.zeros((nt-1,33,33))
        dryflux8km=np.zeros((nt-1,33,33))
        dryflux10km=np.zeros((nt-1,33,33))
        vaporflux5km=np.zeros((nt-1,33,33))
        vaporflux8km=np.zeros((nt-1,33,33))
        vaporflux10km=np.zeros((nt-1,33,33))
        netcondflux5km=np.zeros((nt-1,33,33))
        netcondflux8km=np.zeros((nt-1,33,33))
        netcondflux10km=np.zeros((nt-1,33,33))
        delzmax=np.zeros((nt-1,33,33))
        wmax=np.zeros((nt-1,33,33))
        dryfluxmax=np.zeros((nt-1,33,33))
        vaporfluxmax=np.zeros((nt-1,33,33))
        netcondfluxmax=np.zeros((nt-1,33,33))
        hdelzmax=np.zeros((nt-1,33,33))
        hwmax=np.zeros((nt-1,33,33))
        hdryfluxmax=np.zeros((nt-1,33,33))
        hvaporfluxmax=np.zeros((nt-1,33,33))
        hnetcondfluxmax=np.zeros((nt-1,33,33))

        for t in range(nt-1):
            print t
            w = getvar(wfiles[t],'w')
            ref = getvar(wfiles[t],'ref')
            delz = getvar(wfiles[t+1],'ref')-ref
            dryflux = getvar(fluxfiles[t],'dryflux')
            vaporflux = getvar(fluxfiles[t],'vaporflux')
            netcondflux = getvar(fluxfiles[t],'netcondflux')
            
            height0db[t,:,:] = getheights(ref,height,0)
            height5db[t,:,:] = getheights(ref,height,5)
            height10db[t,:,:] = getheights(ref,height,10)
            height20db[t,:,:] = getheights(ref,height,20)

            w0db[t,:,:] = getvars(w, height, height0db[t,:,:])
            w5db[t,:,:] = getvars(w, height, height5db[t,:,:])
            w10db[t,:,:] = getvars(w, height, height10db[t,:,:])
            w20db[t,:,:] = getvars(w, height, height20db[t,:,:])

            dryflux0db[t,:,:] = getvars(dryflux, height, height0db[t,:,:])
            dryflux5db[t,:,:] = getvars(dryflux, height, height5db[t,:,:])
            dryflux10db[t,:,:] = getvars(dryflux, height, height10db[t,:,:])
            dryflux20db[t,:,:] = getvars(dryflux, height, height20db[t,:,:])

            vaporflux0db[t,:,:] = getvars(vaporflux, height, height0db[t,:,:])
            vaporflux5db[t,:,:] = getvars(vaporflux, height, height5db[t,:,:])
            vaporflux10db[t,:,:] = getvars(vaporflux, height, height10db[t,:,:])
            vaporflux20db[t,:,:] = getvars(vaporflux, height, height20db[t,:,:])

            netcondflux0db[t,:,:] = getvars(netcondflux, height, height0db[t,:,:])
            netcondflux5db[t,:,:] = getvars(netcondflux, height, height5db[t,:,:])
            netcondflux10db[t,:,:] = getvars(netcondflux, height, height10db[t,:,:])
            netcondflux20db[t,:,:] = getvars(netcondflux, height, height20db[t,:,:])

            delz5km[t,:,:] = argheight(delz,height,5000.)
            delz8km[t,:,:] = argheight(delz,height,8000.)
            delz10km[t,:,:] = argheight(delz,height,10000.)

            w5km[t,:,:] = argheight(w,height,5000.)
            w8km[t,:,:] = argheight(w,height,8000.)
            w10km[t,:,:] = argheight(w,height,10000.)

            dryflux5km[t,:,:] = argheight(dryflux,height,5000.)
            dryflux8km[t,:,:] = argheight(dryflux,height,8000.)
            dryflux10km[t,:,:] = argheight(dryflux,height,10000.)

            vaporflux5km[t,:,:] = argheight(vaporflux,height,5000.)
            vaporflux8km[t,:,:] = argheight(vaporflux,height,8000.)
            vaporflux10km[t,:,:] = argheight(vaporflux,height,10000.)

            netcondflux5km[t,:,:] = argheight(netcondflux,height,5000.)
            netcondflux8km[t,:,:] = argheight(netcondflux,height,8000.)
            netcondflux10km[t,:,:] = argheight(netcondflux,height,10000.)

            hdelzmax[t,:,:] = height[np.argmax(delz,0)]
            hwmax[t,:,:] = height[np.argmax(w,0)]
            hdryfluxmax[t,:,:] = height[np.argmax(dryflux,0)]
            hvaporfluxmax[t,:,:] = height[np.argmax(vaporflux,0)]
            hnetcondfluxmax[t,:,:] = height[np.argmax(netcondflux,0)]

            delzmax[t,:,:] = np.max(delz,0)
            wmax[t,:,:] = np.max(w,0)
            dryfluxmax[t,:,:] = np.max(dryflux,0)
            vaporfluxmax[t,:,:] = np.max(vaporflux,0)
            netcondfluxmax[t,:,:] = np.max(netcondflux,0)


        outfilename = time+'-'+xdir+'-2dvars-smoothed3km.h5'
        hf = hdf.File(outfilename,'w')
        hf.create_dataset('height0db',data=height0db)
        hf.create_dataset('height5db',data=height5db)
        hf.create_dataset('height10db',data=height10db)
        hf.create_dataset('height20db',data=height20db)
        hf.create_dataset('w0db',data=w0db)
        hf.create_dataset('w5db',data=w5db)
        hf.create_dataset('w10db',data=w10db)
        hf.create_dataset('w20db',data=w20db)
        hf.create_dataset('dryflux0db',data=dryflux0db)
        hf.create_dataset('dryflux5db',data=dryflux5db)
        hf.create_dataset('dryflux10db',data=dryflux10db)
        hf.create_dataset('dryflux20db',data=dryflux20db)
        hf.create_dataset('vaporflux0db',data=vaporflux0db)
        hf.create_dataset('vaporflux5db',data=vaporflux5db)
        hf.create_dataset('vaporflux10db',data=vaporflux10db)
        hf.create_dataset('vaporflux20db',data=vaporflux20db)
        hf.create_dataset('netcondflux0db',data=netcondflux0db)
        hf.create_dataset('netcondflux5db',data=netcondflux5db)
        hf.create_dataset('netcondflux10db',data=netcondflux10db)
        hf.create_dataset('netcondflux20db',data=netcondflux20db)
        hf.create_dataset('delz5km',data=delz5km)
        hf.create_dataset('delz8km',data=delz8km)
        hf.create_dataset('delz10km',data=delz10km)
        hf.create_dataset('w5km',data=w5km)
        hf.create_dataset('w8km',data=w8km)
        hf.create_dataset('w10km',data=w10km)
        hf.create_dataset('dryflux5km',data=dryflux5km)
        hf.create_dataset('dryflux8km',data=dryflux8km)
        hf.create_dataset('dryflux10km',data=dryflux10km)
        hf.create_dataset('vaporflux5km',data=vaporflux5km)
        hf.create_dataset('vaporflux8km',data=vaporflux8km)
        hf.create_dataset('vaporflux10km',data=vaporflux10km)
        hf.create_dataset('netcondflux5km',data=netcondflux5km)
        hf.create_dataset('netcondflux8km',data=netcondflux8km)
        hf.create_dataset('netcondflux10km',data=netcondflux10km)
        hf.create_dataset('delzmax',data=delzmax)
        hf.create_dataset('wmax',data=wmax)
        hf.create_dataset('dryfluxmax',data=dryfluxmax)
        hf.create_dataset('vaporfluxmax',data=vaporfluxmax)
        hf.create_dataset('netcondfluxmax',data=netcondfluxmax)
        hf.create_dataset('heightdelzmax',data=hdelzmax)
        hf.create_dataset('heightwmax',data=hwmax)
        hf.create_dataset('heightdryfluxmax',data=hdryfluxmax)
        hf.create_dataset('heightvaporfluxmax',data=hvaporfluxmax)
        hf.create_dataset('heightnetcondfluxmax',data=hnetcondfluxmax)
        hf.close()





