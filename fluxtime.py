import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def makesum(varin):
    varout = {}
    for nam in varin.keys():
        x = varin[nam]
        x[np.isnan(x)]=0.
        y=np.cumsum(x)
        varout[nam]=y
    return varout

def coloredplot(modeldirs,var,height,nameout,rh):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((height[xdir],var[xdir]/rh[i]))
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines = LineCollection(lines, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines)
    fig.colorbar(lines)
    ax.autoscale()
    plt.savefig('/nobackup/rstorer/code/timeseriesflux-'+nameout+'-sortedbyprecip-summed-divided-8km.png')
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
    w1 = np.where(colmax>5)
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

#allprecip = {}
#allupdraft = {}
#allflux = {}
for i, dirname in enumerate(dirs):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))
    outdir = '/nobackup/rstorer/code/'
    nt = len(files)
#
#    intup= np.zeros(nt)
#    intpcp= np.zeros(nt)
#    intflux = np.zeros(nt)
#    intnum = 0.
#
#    z = getvar(files[0],'z_coords')
#    zarg = np.argmin(np.abs(z-8000))
#
#    for num in range(1,nt-1):
#        up, pcp, flux = makeplots(files[num],300.,num)
#        intup[num] = up[zarg]
#        intpcp[num] = pcp[zarg]
#        intflux[num] = flux[zarg]
#
#    allflux[dirname] = intflux
#    allupdraft[dirname] = intup
#    allprecip[dirname] = intpcp
#
#
#np.savez('../filesnpz/revutimeseries-flux-netvertical-8km.npz',**allflux)
#np.savez('../filesnpz/revutimeseries-flux-precip-8km.npz',**allprecip)
#np.savez('../filesnpz/revutimeseries-flux-updraft-8km.npz',**allupdraft)
#
sallflux = np.load('../filesnpz/revutimeseries-flux-netvertical-8km.npz')
sallprecip = np.load('../filesnpz/revutimeseries-flux-precip-8km.npz')
sallupdraft = np.load('../filesnpz/revutimeseries-flux-updraft-8km.npz')

allflux = makesum(sallflux)
allprecip = makesum(sallprecip)
allupdraft = makesum(sallupdraft)


height = {}
#allrh = np.load('../filesnpz/rhlow.npz')
allrh = np.load('../filesnpz/totpcpmm.npz')
rh = np.zeros(75)
for i,xdir in enumerate(dirs):
    rh[i]=allrh[xdir]/1000.
    height[xdir] = np.arange(len(allflux[xdir])) *5

coloredplot(dirs,allflux,height,'netvertflux',rh)
coloredplot(dirs,allprecip,height,'precipflux',rh)
coloredplot(dirs,allupdraft,height,'updraftflux',rh)

for i, dirname in enumerate(dirs):
    intup = allupdraft[dirname] 
    if i ==0:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i])
plt.legend()
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Updraft Profiles')
plt.savefig(outdir+'/fluxtime-revu-maxwgt5-allruns-updraft-summed-8km.png')
plt.clf()


for i, dirname in enumerate(dirs):
    intup = allprecip[dirname]
    if i ==0:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i])
plt.legend()
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Precipitation Profiles')
plt.savefig(outdir+'/fluxtime-revu-maxwgt5-allruns-precip-summed-8km.png')
plt.clf()



for i, dirname in enumerate(dirs):
    intup = allflux[dirname]
    if i ==0:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 11')
    elif i ==25:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Aug 17')
    elif i ==50:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i], label = 'Feb 23')
    else:
        plt.plot(height[dirname],intup,linewidth=3, color = cols[i])
plt.legend()
plt.ylabel('km')
plt.xlabel('kg/m$^2$s')
plt.title('Time Average Vertical Condensate Flux Profiles')
plt.savefig(outdir+'/fluxtime-revu-maxwgt5-allruns-netvertical-summed-8km.png')
plt.clf()


net = np.zeros(75)
up = np.zeros(75)
pcp = np.zeros(75)
for i,dirname in enumerate(dirs):
    net[i]=allflux[dirname][-1]/rh[i]
    up[i]=allupdraft[dirname][-1]/rh[i]
    pcp[i]=allprecip[dirname][-1]/rh[i]



plt.scatter(rh,net)
p = np.poly1d(np.polyfit(rh,net,2))
variance = np.var(net)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,net)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/fluxscatter-revu-maxwgt5-allruns-netvertical-summed-8km-precip.png')
plt.clf()

plt.scatter(rh,up)
p = np.poly1d(np.polyfit(rh,up,2))
variance = np.var(up)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,up)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/fluxscatter-revu-maxwgt5-allruns-updraft-summed-8km-precip.png')
plt.clf()

plt.scatter(rh,pcp)
p = np.poly1d(np.polyfit(rh,pcp,2))
variance = np.var(pcp)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,pcp)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/fluxscatter-revu-maxwgt5-allruns-precip-summed-8km-precip.png')
plt.clf()


