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
    return diff, vert1, micro2,w1

def makeplots(fil1,fil2,mlist,dt,num):
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    diff,vertflux,micro,w = getbudgetvars(fil1,fil2,mlist,dt)
    vert = np.diff(vertflux,axis=0)
    colmax = np.max(w,0)
    w1 = np.where(colmax>5)
    w0 = np.where(colmax <= 5)
    diff1 = diff[:,w1[0],w1[1]]
    diff0 = diff[:,w0[0],w0[1]]
    vert1 = vert[:,w1[0],w1[1]]
    vert0 = vert[:,w0[0],w0[1]]
    flux = vertflux[:,w1[0],w1[1]]
    micro1 = micro[:,w1[0],w1[1]]
    micro0 = micro[:,w0[0],w0[1]]
    height = getvar(fil1,'z_coords')
    mdiff1 = np.mean(diff1,1)
    mdiff0 = np.mean(diff0,1)
    mvert1 = np.mean(vert1,1)
    mvert0 = np.mean(vert0,1)
    mmicro1 = np.mean(micro1,1)
    mmicro0 = np.mean(micro0,1)
    diffprof = np.mean(np.mean(diff,1),1)
    vertprof = np.mean(np.mean(vert,1),1)
    micprof = np.mean(np.mean(micro,1),1)


    plt.plot(diffprof[37:],height[37:],color = 'black',linewidth=3,label = 'mass diff')
    plt.plot(vertprof[37:],height[38:],color = 'red', linewidth =3, label = 'vertical flux divergence')
    plt.plot(micprof[37:], height[37:], color = 'blue', linewidth=3, label = 'micro')
    plt.legend()
    plt.title('all profiles')
    plt.savefig('/nobackup/rstorer/plots/profilesall-'+outnum+'.png')
    plt.clf()


    plt.plot(mdiff1,height,color = 'black',label = 'mass diff',linewidth=3)
    plt.plot(mdiff0,height,color = 'black',linestyle = 'dashed',linewidth=3)
    plt.plot(mvert1[1:],height[1:-1],color = 'red',label = 'vertical flux divergence',linewidth=3)
    plt.plot(mvert0[1:],height[1:-1],color = 'red',linestyle = 'dashed',linewidth=3)
    plt.plot(mmicro1,height,color = 'blue',label = 'micro',linewidth=3)
    plt.plot(mmicro0,height,color = 'blue',linestyle = 'dashed',linewidth=3)
    plt.legend()
    plt.savefig('/nobackup/rstorer/plots/profiles5-'+outnum+'.png')
    plt.clf()

    intdiff = np.zeros_like(mdiff1)
    intmicro = np.zeros_like(mmicro1)
    intflux = np.mean(flux,1)
    for z in range(82):
        intdiff[z] = np.sum(mdiff1[z:])
        intmicro[z] = np.sum(mmicro1[z:])
    plt.plot(intdiff[37:],height[37:], color = 'black', linewidth=3, label = 'mass diff')
    plt.plot(intmicro[37:],height[37:], color = 'blue', linewidth = 3, label = 'micro')
    plt.plot(intflux[37:],height[37:],color = 'red', linewidth = 3, label = 'flux')
    plt.plot(intmicro[37:]+intflux[37:],height[37:], color = 'green', linewidth=3, label = 'sum')
    plt.xlim(-.006,.010)
    plt.legend()
    plt.title('integrated')
    plt.savefig('/nobackup/rstorer/plots/profilesintegrated5-'+outnum+'.png')
    plt.clf()
    
    




files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/feb*h5'))
outdir = '/nobackup/rstorer/plots/'

#makeplots(files[3],files[4],[files[4]],30.)

for num in range(1,len(files)-1):
    makeplots(files[num],files[num+1],[files[num+1]],30.,num)

#makeplots(files[1],files[3],files[2:4],60.)
#makeplots(files[1],files[4],files[2:5],90.)
#makeplots(files[1],files[5],files[2:6],120.)
#makeplots(files[1],files[6],files[2:7],150.)
#makeplots(files[1],files[7],files[2:8],180.)
#makeplots(files[1],files[11],files[2:12],300.)



z=getvar(files[0],'z_coords')
for i in range(37,len(z)):
    print i, z[i]




