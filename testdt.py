import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar
import glob
from rachelutils.hdfload import getdz

def getbudgetvars(fil1,fil2,mlist,dt):
    cond1 = getvar(fil1, 'total_cond')/1000.
    cond2 = getvar(fil2, 'total_cond')/1000.
    rho1 = (getvar(fil1, 'press') * 100.) / (getvar(fil1, 'tempk') *287.)
    rho2 = (getvar(fil2, 'press') * 100.) / (getvar(fil2, 'tempk') *287.)
    w1 = getvar(fil1, 'w')
    micro2 = np.zeros_like(w1)
    for files in mlist:
        micro2 = micro2+ getvar(files, 'nuccldrt') + getvar(files, 'nucicert') + getvar(files, 'vapliqt') + getvar(files, 'vapicet')
    pcp1 = getvar(fil1, 'precip3d')
    dz = getdz(fil1)
    micro2 = (micro2*rho2*dz[:,None,None])/(dt*1000)
    massflux1 = cond1*rho1*w1
    diff = ((cond2*rho2*dz[:,None,None])-(cond1*rho1*dz[:,None,None]))/dt
    vert1 = massflux1-pcp1
    return diff, vert1, micro2

def makeplots(fil1,fil2,mlist,dt):
    diff,vert,micro = getbudgetvars(fil1,fil2,mlist,dt)
    diff = diff[:,170,:]
    vert = vert[:,170,:]
    micro = micro[:,170,:]
#    diff = np.mean(diff[:,160:171,:],1)
#    vert = np.mean(vert[:,160:171,:],1)
#    micro = np.mean(micro[:,160:171,:],1)
    bigarray =np.concatenate((diff, vert, micro),axis=0)
    getmax = np.max(bigarray)
    getmin = np.min(bigarray)

    levels = np.linspace(getmin,getmax,20)
    height = getvar(fil1,'z_coords')
    xs = np.arange(400)*.25

    plt.subplot(3,1,1)
    plt.contourf(xs[160:320], height, diff[:,160:320])
    plt.ylim(0,18000)
    plt.title('mass diff')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])

    plt.subplot(3,1,2)
    plt.contourf(xs[160:320], height, vert[:,160:320]) 
    plt.ylim(0,18000)
    plt.title('net vertical flux')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])

    plt.subplot(3,1,3)
    plt.contourf(xs[160:320], height, micro[:,160:320]) 
    plt.ylim(0,18000)
    plt.title('micro')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])
    plt.savefig(outdir+str(dt)+'diffs.png')
    plt.clf()

#    permicro = micro/diff
#    pervert = vert/diff
#    permicro[np.isnan(permicro)]=0
#    pervert[np.isnan(pervert)]=0
    leftover = diff - (micro+vert)

    plt.subplot(3,1,1)
    plt.contourf(xs[160:320], height, diff[:,160:320])
    plt.ylim(0,18000)
    plt.title('diff')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])

    plt.subplot(3,1,2)
    plt.contourf(xs[160:320], height, (vert[:,160:320]+micro[:,160:320]))
    plt.ylim(0,18000)
    plt.title('vertical+micro')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])

    plt.subplot(3,1,3)
    plt.contourf(xs[160:320], height, leftover[:,160:320])
    plt.ylim(0,18000)
    plt.title('leftover ')
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])
    plt.savefig(outdir+str(dt)+'partofdiff.png')
    plt.clf()




files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/feb*h5'))
outdir = '/nobackup/rstorer/plots/budgetslices/'

makeplots(files[1],files[2],[files[2]],30.)
makeplots(files[1],files[3],files[2:4],60.)
makeplots(files[1],files[4],files[2:5],90.)
makeplots(files[1],files[5],files[2:6],120.)
makeplots(files[1],files[6],files[2:7],150.)
makeplots(files[1],files[7],files[2:8],180.)
makeplots(files[1],files[11],files[2:12],300.)








