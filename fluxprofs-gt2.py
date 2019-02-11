import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def coloredplot(modeldirs,var,height,nameout,rh):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((var[xdir],height))
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines)
    fig.colorbar(lines)
    ax.set_ylim(0,20)
    ax.autoscale()
    plt.savefig('/nobackup/rstorer/plots/avgprof-'+nameout+'-sortedbyrhlow-gt2.png')
    plt.close()

def getbudgetvars(fil1,dt):
    cond = getvar(fil1, 'total_cond')/1000.
    rho = (getvar(fil1, 'press') * 100.) / (getvar(fil1, 'tempk') *287.)
    w = getvar(fil1, 'w')
    pcp = getvar(fil1, 'precip3d') * -1
    dz = getdz(fil1)
    massflux = cond*rho*w
    return massflux,w,pcp

def makeplots(fil1,dt,num):
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    upflux,w,pcp= getbudgetvars(fil1,dt)
    colmax = np.max(w,0)
    w1 = np.where(colmax>2)
    flux = upflux  + pcp

    updraft = upflux[:,w1[0],w1[1]]
    precip = pcp[:,w1[0],w1[1]]
    vert = flux[:,w1[0],w1[1]]

    netvert = np.mean(vert,1)
    up = np.mean(updraft,1)
    pre = np.mean(precip,1)

    return up, pre, netvert

dirs = pert75()
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')

allprecip = {}
allupdraft = {}
allflux = {}
for i, dirname in enumerate(dirs):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/'+dirname+'*h5'))
    outdir = '/nobackup/rstorer/code/'

    intup= np.zeros(82)
    intpcp= np.zeros(82)
    intflux = np.zeros(82)
    intnum = 0.

    for num in range(1,len(files)-1):
        up, pcp, flux = makeplots(files[num],300.,num)
        if np.max(flux) >0:
            intup = intup + up
            intpcp = intpcp + pcp
            intflux = intflux + flux
            intnum +=1
    intup = intup / intnum
    intpcp = intpcp / intnum
    intflux = intflux / intnum

    allflux[dirname] = intflux
    allupdraft[dirname] = intup
    allprecip[dirname] = intpcp


np.savez('revuprofile-flux-netvertical-gt2.npz',**allflux)
np.savez('revuprofile-flux-precip-gt2.npz',**allprecip)
np.savez('revuprofile-flux-updraft-gt2.npz',**allupdraft)

#allflux = np.load('revuprofile-flux-netvertical-gt2.npz')
#allprecip = np.load('revuprofile-flux-precip-gt2.npz')
#allupdraft = np.load('revuprofile-flux-updraft-gt2.npz')

#allvapor = np.load('revuprofile-flux-updraft-vapor-gt2.npz')


height = getvar(files[0], 'z_coords')/1000.

allrh = np.load('rhlow.npz')
rh = np.zeros(75)
for i,xdir in enumerate(dirs):
    rh[i]=allrh[xdir]

coloredplot(dirs,allflux,height,'netvertflux',rh)
coloredplot(dirs,allprecip,height,'precipflux',rh)
coloredplot(dirs,allupdraft,height,'updraftflux',rh)

for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allvapor[dirname]
    if i ==0:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
plt.legend()
plt.ylim([0,20])
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Updraft Profiles')
plt.savefig(outdir+'/fluxprofs-revu-maxwgt5-allruns-updraft-vapandcond-gt2.png')
plt.clf()


for i, dirname in enumerate(dirs):
    intup = allprecip[dirname]
    if i ==0:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
plt.legend()
plt.ylim([0,20])
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Precipitation Profiles')
plt.savefig(outdir+'/fluxprofs-revu-maxwgt5-allruns-precip-gt2.png')
plt.clf()



for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] + allvapor[dirname] + allprecip[dirname]
    if i ==0:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(intup[1:],height[1:], linewidth=3, color = cols[i])
plt.legend()
plt.ylim([0,20])
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Vertical Condensate Flux Profiles')
plt.savefig(outdir+'/fluxprofs-revu-maxwgt5-allruns-netvertical-vapandcond-gt2.png')
plt.clf()










