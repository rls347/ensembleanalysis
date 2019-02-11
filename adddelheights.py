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
        delheight0db=np.zeros((nt-1,33,33))
        delheight5db=np.zeros((nt-1,33,33))
        delheight10db=np.zeros((nt-1,33,33))
        delheight20db=np.zeros((nt-1,33,33))
        
        for t in range(nt-1):
            print t
            w = getvar(wfiles[t],'w')
            ref = getvar(wfiles[t],'ref')
            ref2 = getvar(wfiles[t+1],'ref')
            
            height0db = getheights(ref,height,0)
            height5db = getheights(ref,height,5)
            height10db = getheights(ref,height,10)
            height20db = getheights(ref,height,20)

            theight0db = getheights(ref2,height,0)
            theight5db = getheights(ref2,height,5)
            theight10db = getheights(ref2,height,10)
            theight20db = getheights(ref2,height,20)

            delheight0db[t,:,:] = theight0db - height0db
            delheight5db[t,:,:] = theight5db - height5db
            delheight10db[t,:,:] = theight10db - height10db
            delheight20db[t,:,:] = theight20db - height20db



        outfilename = '../h5files/'+time+'/'+time+'-'+xdir+'-2dvars-smoothed3km.h5'
        hf = hdf.File(outfilename,'a')
        hf.create_dataset('delheight0db',data=delheight0db)
        hf.create_dataset('delheight5db',data=delheight5db)
        hf.create_dataset('delheight10db',data=delheight10db)
        hf.create_dataset('delheight20db',data=delheight20db)
        hf.close()





