import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import glob
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar, getdz

def makearray(d,dirs):
    a = np.zeros(75)
    for i, xdir in enumerate(dirs):
        a[i] = d[xdir]
    return a

def coloredplot(var,height,modeldirs, nameout,rh):
    height=height/1000.
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((var[xdir],height))
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines1 = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=3,alpha=.7)
    ax.add_collection(lines1)
    fig.colorbar(lines1,label='RH')
    ax.set_xlabel('Tracer Flux (#/m$^2$s)')
    ax.set_ylabel('Height (km)')
    ax.set_title('Average Updraft Tracer Flux')
    ax.set_ylim(0,16)
    ax.set_xlim(-1000000000.0, 4000000000.0)

    ax2 = fig.add_axes([.4,.4,.3,.4])
    lines2 = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=2,alpha=.7)
    ax2.add_collection(lines2)
    ax2.set_ylim(5,16)
    ax2.set_xlim(-100000000.0, 500000000.0)

    plt.savefig(nameout)
    plt.close()
    return


def plotprofiles(var, height, modeldirs, filename, rh):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((var[xdir],height))
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines1 = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=3)
    ax.add_collection(lines1)
    ax.set_xlim(-6000000000,6000000000)
    ax.set_ylim(0,18000)
    print filename
    tmp = []
    for xdir in modeldirs:
        tmp.append(np.min(var[xdir]))
    plt.savefig(filename)
    plt.clf()
    return

def plotscatter(yd,rh, dirs, filename, initval):
    i = makearray(initval, dirs)
    y = makearray(yd,dirs)
    y=y/i
    plt.scatter(rh,y)
    plt.savefig(filename)
    plt.clf()

    logx = rh
    logy = np.log(y)
    logx = logx[~np.isnan(logy)]
    logy = logy[~np.isnan(logy)]

    thresh = np.mean(logy)-(2*np.std(logy))
    plogx = logx#[logy>thresh]
    plogy = logy#[logy>thresh]

    plt.scatter(logx,logy)
    p = np.poly1d(np.polyfit(plogx,plogy,1))
    a,b = np.polyfit(plogx,plogy,1)
    variance = np.var(plogy)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(plogx,plogy)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(logx.min(),logx.max(),100)
    plt.plot(xp,p(xp))
    ax = plt.gca()
    ax.set_ylabel('log(Tracer Flux) (#/m$^2$)')
    ax.set_xlabel('Low Level RH (%)')
    ax.set_title('Integrated Tracer Flux at 8 km')
    plt.text(.2,.7,'$R^2 = %0.2f$'% Rsqr ,fontweight='bold',color ='black',transform = ax.transAxes)
    plt.savefig(filename+'logfit.png')
    plt.clf()



    plt.subplot(2,1,1)
    plt.scatter(rh,y)
    p = np.poly1d(np.polyfit(plogx,plogy,1))
    plt.title('Integrated Tracer Flux at 8 km',size=18)
    plt.ylabel('Tracer Flux (/m$^2$)')
    ax = plt.gca()
    plt.subplot(2,1,2)
    plt.scatter(logx,logy)
    variance = np.var(plogy)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(plogx,plogy)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(logx.min(),logx.max(),100)
    plt.plot(xp,p(xp))
    ax = plt.gca()
    ax.yaxis.labelpad=20
    ax.set_ylabel('ln(Tracer Flux)')
    ax.set_xlabel('Low Level RH (%)')
    ff=plt.text(.2,.7,'$R^2 = %0.2f$'% Rsqr ,color ='black',size=13,weight='black',transform = ax.transAxes)
    plt.savefig(filename+'2panel.png')
    plt.clf()

    plt.scatter(rh,y)
    print len(rh), len(y)
    yvar = np.poly1d(np.polyfit(rh,y,2))
    plt.plot(xp,yvar(xp))
    resituals = np.var([(p(xx)-yy) for xx, yy in zip(rh,y)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    ff=plt.text(.2,.7,'$R^2 = %0.2f$'% Rsqr ,color ='black',size=13,weight='black',transform = ax.transAxes)
    plt.title('Integrated Tracer Flux at 8 km',size=18)
    plt.ylabel('Tracer Flux (/m$^2$)')
    plt.xlabel('Low Level RH (%)')

    plt.savefig(filename+'logtest.png')
    plt.clf()


    return

def makesum(x2d,zarg):
    x = x2d[:,zarg]
    x[np.isnan(x)]=0.
    x = x*300
    y=np.cumsum(x)
    return y[-1]


def gettimeprofs(xdir):
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'*h5'))
    nt = len(files)
    z = getvar(files[0],'z_coords')
    zarg = np.argmin(np.abs(z-8000))
    nz = len(z)
    outvar2 = np.zeros((nt,nz))
    outvar5 = np.zeros((nt,nz))
    tmpprof = np.zeros((nt,nz))
    for t, fil in enumerate(files):
        cond = getvar(fil, 'tracer002')*100.*100.*100.
        w = getvar(fil, 'w')
        massflux = cond*w

        colmax = np.max(w,0)
        w2 = np.where(colmax>2)
        w5 = np.where(colmax>5)
       
        if np.max(w)>5:
            updraft5 = massflux[:,w5[0],w5[1]]
            up5 = np.mean(updraft5,1)    
            outvar5[t,:]=up5
        updraft2 = massflux[:,w2[0],w2[1]]
        up2 = np.mean(updraft2,1)
        outvar2[t,:] = up2
        ttm = massflux[:,w5[0],w5[1]]
        tmpprof[t,:] = np.mean(ttm,1)

    return outvar2, outvar5

def get8kmflux(xdir):
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'*h5'))
    nt = len(files)
    z = getvar(files[0],'z_coords')
    zarg = np.argmin(np.abs(z-8000))
    values5 = np.zeros(nt)
    values2 = np.zeros(nt)

    for t, fil in enumerate(files):
        cond = getvar(fil, 'tracer002')[zarg,:,:]*100.*100.*100.
        w = getvar(fil, 'w')
        massflux = cond*w[zarg,:,:]

        colmax = np.max(w,0)
        w2 = np.where(colmax>2)
        w5 = np.where(colmax>5)

        if np.max(w)>5:
            updraft5 = massflux[w5[0],w5[1]]
            up5 = np.sum(updraft5)*250*250
            values5[t]=up5
        if np.max(w)>2:
            updraft2 = massflux[w2[0],w2[1]]
            up2 = np.sum(updraft2)*250*250
            values2[t] = up2

    return values2,values5

    

z = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords') 
zarg = np.argmin(np.abs(z-8000))

dirs = pert75()
#these are nt x nz...one average profile at each time
var2d5={}
var2d2={}
#for xdir in dirs:
#    x2,x5 = gettimeprofs(xdir)
#    var2d5[xdir] = x5
#    var2d2[xdir] = x2

#np.savez('newtracerprofiles-2d-wgt2.npz',**var2d2)
#np.savez('newtracerprofiles-2d-wgt5.npz',**var2d5)

var2d2 = np.load('newtracerprofiles-2d-wgt2.npz')
var2d5 = np.load('newtracerprofiles-2d-wgt5.npz')

#get average profile that goes in plot with zoom...
meanprof2 = {}
meanprof5 = {}
for xdir in dirs:
    p2 = np.nanmean(var2d2[xdir],0)
    p5 = np.nanmean(var2d5[xdir],0)
    meanprof2[xdir] = p2
    meanprof5[xdir] = p5

np.savez('newtracerprofiles-meanprof-wgt2.npz', **meanprof2)
np.savez('newtracerprofiles-meanprof-wgt5.npz', **meanprof5)

#meanprof2 = np.load('newtracerprofiles-meanprof-wgt2.npz')
#meanprof5 = np.load('newtracerprofiles-meanprof-wgt5.npz')

y2 = {}
y5 = {}
#make time series of 8km flux and get cumulative sum for powerlaw plot
for xdir in dirs:
    y2[xdir] = makesum(var2d2[xdir],zarg)
    y5[xdir] = makesum(var2d5[xdir],zarg)


#get initial values of tracer to weight flux by
initval = {}
for xdir in dirs:
    fil = '/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5'
    t0 = getvar(fil,'tracer002')[:,100,100]
    dz = getdz(fil)
    x = t0*dz*100*100*100
    initval[xdir]=np.sum(x)


rh0 = np.load('rhlow.npz')
rh = makearray(rh0, dirs) 

plotprofiles(meanprof2, z, dirs, 'newtracerprofileswgt2.png', rh)
plotprofiles(meanprof5, z, dirs, 'newtracerprofileswgt5.png', rh)

#plotscatter(y2, rh, dirs, 'newtracerprofiles-scatter-wgt2.png', initval)
#plotscatter(y5, rh, dirs, 'newtracerprofiles-scatter-wgt5.png', initval)



coloredplot(meanprof2, z, dirs, 'newtracerprofileswgt2-zoom.png', rh)
coloredplot(meanprof5, z, dirs, 'newtracerprofileswgt5-zoom.png', rh)





#var1 = np.load('../filesnpz/budget-timeseries-updrafttracer2flux.npz')
#var2 = np.load('../filesnpz/budget-total-updrafttracer2flux.npz')
#var3 = np.load('../filesnpz/revuprofile-flux-updraft-tracer.npz')
#var4 = np.load('../filesnpz/revutimeseries-flux-updraft-profiles-tracer2.npz')
#var5 = np.load('../filesnpz/revutimeseries-flux-updraft-profiles-tracer2-gt5.npz')
#var6 = np.load('newmeanprofstracer.npz')
#var7 = np.load('total2dprof-tracer002.npz')
#var8 = np.load('tracer002-updraftflux-wgt5-updraftarea.npz')
#var9 = np.load('tracer002-updraftflux-wgt5.npz')
#var10 = np.load('tracer002_total8kmflux_number.npz')
#
#
#v1=var1[xdir]
#v2=var2[xdir]
#v3=var3[xdir]
#v4=var4[xdir]
#v5=var5[xdir]
#v6=var6[xdir]
#v7=var7[xdir]
#v8=var8[xdir]
#v9=var9[xdir]
#v10=var10[xdir]
#
#
#abc,bbc,bbc2 = gettimeprofs(xdir)
#doing the mean without checking for empty/nan led to bigger numbers seen in file 9 for instance...fixed this here.

times5 = {}
times2 = {}

pval5 = {} 
pval2 = {}

#for i,xdir in enumerate(dirs):
#    values2, values5 = get8kmflux(xdir)
#    times5[xdir] = values5
#    times2[xdir] = values2
#    a5 = np.cumsum(values5)*300
#    pval5[xdir]=a5[-1]
#    a2 = np.cumsum(values2)*300
#    pval2[xdir]=a2[-1]

#np.savez('newtracerprofiles-flux8kmtimeseries-wgt2.npz',**times2)
#np.savez('newtracerprofiles-flux8kmtimeseries-wgt5.npz',**times5)

times2 = np.load('newtracerprofiles-flux8kmtimeseries-wgt2.npz')
times5 = np.load('newtracerprofiles-flux8kmtimeseries-wgt5.npz')

for xdir in dirs:
    values5 = times5[xdir]
    values2 = times2[xdir]
    a5 = np.cumsum(values5)*300
    a2 = np.cumsum(values2)*300
    pval5[xdir]=a5[-1]
    pval2[xdir]=a2[-1]


plotscatter(pval5,rh, dirs, 'newtracerprofiles-scatter-wgt5', initval)
plotscatter(pval2,rh, dirs, 'newtracerprofiles-scatter-wgt2', initval)





