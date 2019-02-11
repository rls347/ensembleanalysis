import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar
import glob
from rachelutils.hdfload import getdz

def calcadvflux(fil):
    u=getvar(fil,'u')
    v=getvar(fil,'v')
    q=getvar(fil,'total_cond')/1000.
    p=getvar(fil,'press')
    t=getvar(fil,'tempk')
    rho = (p*100.)/(t*287.)
    umean = np.mean(np.mean(u,1),1)
    vmean = np.mean(np.mean(v,1),1)
    uprime = u-umean[:,None,None]
    vprime = v-vmean[:,None,None]
    uflux=rho*q*uprime
    vflux=rho*q*vprime
    uadv = rho*q*umean[:,None,None]
    vadv = rho*q*vmean[:,None,None]
    return uflux, vflux,uadv,vadv

def advprofiles(fil,u,v):
    w=getvar(fil,'w')
    wmax = np.max(w[37:,:,:],0)
    advprofs = np.zeros(82)
    ii=200
    jj=200
    uleft = u[:,ii-100:ii+100,jj-100]
    uright=u[:,ii-100:ii+100,jj+100]
    udiff = (uleft-uright)/200.
    vbottom=v[:,ii-100,jj-100:jj+100]
    vtop=v[:,ii+100,jj-100:jj+100]
    vdiff = (vbottom-vtop)/200.
    advprofs=udiff+vdiff
    return advprofs

def getbudgetvars(fil1,fil2,mlist,dt):
    dz = getdz(fil1)
    cond1 = getvar(fil1, 'total_cond')/1000.
    cond2 = getvar(fil2, 'total_cond')/1000.
    rho1 = (getvar(fil1, 'press') * 100.) / (getvar(fil1, 'tempk') *287.)
    rho2 = (getvar(fil2, 'press') * 100.) / (getvar(fil2, 'tempk') *287.)
    w1 = getvar(fil1, 'w')
    micro2 = np.zeros_like(w1)
    for files in mlist:
        micro2 = micro2+ getvar(files, 'nuccldrt') + getvar(files, 'nucicert') + getvar(files, 'vapliqt') + getvar(files, 'vapicet')
    pcp1 = getvar(fil1, 'precip3d')
    micro2 = (micro2*rho2*dz[:,None,None])/(dt*1000)
    massflux1 = cond1*rho1*w1
    diff = ((cond2*rho2*dz[:,None,None])-(cond1*rho1*dz[:,None,None]))/dt
    vert1 = massflux1-pcp1
    return diff, vert1, micro2,w1,massflux1,pcp1

def makeplots(fil1,fil2,mlist,dt,num):
    dz = getdz(fil1)
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    diff,vertflux,micro,w,cmf,pcp = getbudgetvars(fil1,fil2,mlist,dt)
    udet,vdet,uadv,vadv=calcadvflux(fil1)
    advprofs = advprofiles(fil1,uadv,vadv)
    detprofs = advprofiles(fil1,udet,vdet)
    vert = np.diff(vertflux,axis=0) * -1
    diff1 = diff[:,100:300,100:300]
    vert1 = vert[:,100:300,100:300]
    flux = vertflux[:,100:300,100:300] * 250 * 250
    updraftonly = cmf[:,100:300,100:300]*250*250
    pcponly = pcp[:,100:300,100:300]*250*250
    micro1 = micro[:,100:300,100:300]
    height = getvar(fil1,'z_coords')
    diffprof = np.sum(np.sum(diff1,1),1) * 250*250
    vertprof = np.sum(np.sum(vert1,1),1) * 250*250
    micprof = np.sum(np.sum(micro1,1),1) * 250*250
    advprof = np.sum(advprofs,1) * dz * 250
    detprof = np.sum(detprofs,1) * dz * 250

    intdiff = np.zeros_like(diffprof)
    intmicro = np.zeros_like(diffprof)
    intadv = np.zeros_like(diffprof)
    intdet = np.zeros_like(diffprof)
    intflux = np.sum(np.sum(flux,1),1)
    intpcp = np.sum(np.sum(pcponly,1),1)*-1
    intcmf = np.sum(np.sum(updraftonly,1),1)
    testvert = np.zeros_like(diffprof)

    for z in range(82):
        intdiff[z] = np.sum(diffprof[z:])
        intmicro[z] = np.sum(micprof[z:])
        intadv[z] = np.sum(advprof[z:])
        intdet[z] = np.sum(detprof[z:])
        testvert[z] = np.sum(vertprof[z:])
    print intmicro.shape, intflux.shape, intadv.shape, intdet.shape
    sumvar = intmicro+intflux+intadv+intdet
        
    plt.plot(intdiff[37:],height[37:], color = 'black', linewidth=3, label = 'mass diff')
    plt.plot(intmicro[37:],height[37:], color = 'blue', linewidth = 3, label = 'micro')
    plt.plot(intflux[37:],height[37:],color = 'red', linewidth = 3, label = 'flux')
    plt.plot(testvert[37:],height[37:],color = 'black',linewidth=2,linestyle='dashed',label='fluxtestint')
    plt.plot(intpcp[37:],height[37:],color = 'gray', linewidth = 3, label = 'pcp')
    plt.plot(intcmf[37:],height[37:],color = 'orange', linewidth = 3, label = 'updraft')
    plt.plot(intadv[37:],height[37:],color = 'green', linewidth = 3, label = 'advection')
    plt.plot(intdet[37:],height[37:],color = 'yellow', linewidth=3, label = 'detrainment')
    plt.plot(sumvar[37:],height[37:], color = 'purple', linewidth=3, label = 'sum')
#    plt.xlim(-.006,.010)
#    plt.xlim(-400,500)
    plt.legend()
    plt.title('integrated')
    plt.savefig('/nobackup/rstorer/plots/budgetslices/bigdomainsplitadvectionprofilesintegrated5-'+outnum+'.png')
    plt.clf()

    return intdiff[46],intmicro[46],intadv[46],intflux[46]


    
    




files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/feb*h5'))
outdir = '/nobackup/rstorer/plots/budgetslices/'

diff=np.zeros(len(files)-2)
micro = np.zeros_like(diff)
adv = np.zeros_like(diff)
flux = np.zeros_like(diff)

for num in range(1,len(files)-1):
    d,m,a,f = makeplots(files[num],files[num+1],[files[num+1]],30.,num)
    diff[num-1]=d
    micro[num-1]=m
    adv[num-1]=a
    flux[num-1]=f

plt.plot(diff,linewidth=3,color='black',label='massdiff')
plt.plot(micro,color = 'blue', linewidth = 3, label = 'micro')
plt.plot(adv,color = 'green', linewidth = 3, label = 'advection')
plt.plot(flux, color = 'red', linewidth = 3, label = 'flux')
plt.plot((diff+micro+adv+flux), color = 'purple', linewidth=3, label = 'sum')
plt.legend()
plt.savefig('/nobackup/rstorer/plots/budgetslices/splitincludingadv-timeseriesbudget.png')
plt.clf()

