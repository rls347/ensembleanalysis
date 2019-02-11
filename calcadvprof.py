import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
import glob
from rachelutils.hdfload import getvar

def calcadvflux(fil):
    u=getvar(fil,'u')
    v=getvar(fil,'v')
    q=getvar(fil,'total_cond')
    p=getvar(fil,'press')
    t=getvar(fil,'tempk')
    rho = (p*100.)/(t*287.)
    umean = np.mean(np.mean(u,1),1)
    vmean = np.mean(np.mean(v,1),1)
    uprime = u-umean[:,None,None]
    vprime = v-vmean[:,None,None]
    uflux=rho*umean[:,None,None]*q
    vflux=rho*vmean[:,None,None]*q
    return uflux, vflux

def advprofiles(fil,u,v):
    w=getvar(fil,'w')
    wmax = np.max(w[37:,:,:],0)
    vals = np.where(wmax>5)
    nprofs = len(vals[0])
    print nprofs
    advprofs = np.zeros((82,nprofs))
    for i in range(nprofs):
        ii=vals[0][i]
        jj=vals[1][i]
        udiff=u[:,ii,jj-1]-u[:,ii,jj+1]
        vdiff=v[:,ii-1,jj]-v[:,ii+1,jj]
        advprofs[:,i]=udiff+vdiff
    return advprofs

def plotadvprof(fil):
    height = getvar(fil,'z_coords')
    uflux,vflux = calcadvflux(fil)
    advprofs = advprofiles(fil,uflux,vflux)
    meanprof = np.mean(advprofs,1)
    plt.plot(meanprof,height,linewidth=2)

files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/*h5'))
for filename in files:
    fil = hdf.File(filename,'r')
    plotadvprof(fil)
    fil.close()
plt.savefig('/nobackup/rstorer/plots/budgetslices/advectionprofiles-onlymeanwind-w5.png')
plt.clf()

