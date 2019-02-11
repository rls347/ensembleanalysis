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
        x = x*300
        y=np.cumsum(x)
        varout[nam]=y
    return varout

def coloredplot(modeldirs,var,height,nameout,rh):
    plotvars = []
    for i,xdir in enumerate(modeldirs):
        plotvars.append((var[xdir],height[xdir]))
        print var[xdir]
    lines = [zip(x,y) for x, y in plotvars]
    fig, ax = plt.subplots()
    lines1 = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=3)
    ax.add_collection(lines1)
    fig.colorbar(lines1,label='RH')
    ax.set_xlabel('Tracer Flux (#/m$^2$s)')
    ax.set_ylabel('Height (km)')
    ax.set_title('Average Updraft Tracer Flux')
    ax.set_ylim(0,16)
    ax.set_xlim(-900000000.0, 7000000000.0)

    ax2 = fig.add_axes([.4,.4,.3,.4])
    lines2 = LineCollection(lines, array = rh, cmap = plt.cm.plasma, linewidth=2)
    ax2.add_collection(lines2)
    ax2.set_ylim(5,16)
    ax2.set_xlim(-90000000.0, 800000000.0)

#    ax.autoscale()
#    plt.savefig('/nobackup/rstorer/plots/fluxprof-updraftavg-'+nameout+'-sortedbyrhlow-tracer2-upper-1000-900-tavg-test97gt2.png')
    plt.savefig('newfluxprof-wholeandzoomed-gt2.png')
    plt.close()

def getbudgetvars(fil1,dt):
    cond = getvar(fil1, 'tracer002')*100.*100.*100.
    w = getvar(fil1, 'w')
    dz = getdz(fil1)
    massflux = cond*w
    return massflux,w

def makeplots(fil1,dt,num):
    outnum = str(num)
    if num<10:
        outnum = '0'+outnum
    upflux,w= getbudgetvars(fil1,dt)
    colmax = np.max(w,0)
    w1 = np.where(colmax>2)

    updraft = upflux[:,w1[0],w1[1]]

    up = np.mean(updraft,1)

    return up

dirs = pert75()
#dirs = ['feb23-control']
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')

sallupdraft={}
initval = {}
profs = {}
for i, dirname in enumerate(dirs):
    print dirname
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/'+dirname+'*h5'))
#    #outdir = '/nobackup/rstorer/plots/'
    outdir = '.'
    nt = len(files)
    t2 = getvar(files[0],'tracer002')[:,100,100]
    dz = getdz(files[0])
    x = t2*dz*100*100*100
    initval[dirname]=np.sum(x)
#    profs[dirname]=t2
#
#    intup= np.zeros((nt,82))
#    intnum = 0.
#
    z = getvar(files[0],'z_coords')
    zarg = np.argmin(np.abs(z-8000))
#
#    for num in range(1,nt-1):
#        up= makeplots(files[num],300.,num)
#        intup[num,:] = up
#        
#    avgintup = np.nanmean(intup,0)
#    sallupdraft[dirname] = avgintup

#np.savez('newmeanprofstracer.npz',**sallupdraft)
profiles = np.load('newmeanprofstracer.npz')
sallupdraft = {}
allupdraft = {}
for xdir in dirs:
    allupdraft[xdir] = profiles[xdir][zarg]

#allupdraft = makesum(sallupdraft)
zvals = getvar(files[0],'z_coords')/1000.
height = {}
precipvals= np.load('../filesnpz/totpcpmm.npz')
rh = np.zeros(75)
pcp = np.zeros(75)
init_trac = np.zeros(75)
rhvars = np.load('rhlow.npz')

freetrop = np.zeros(75)
for i, xdir in enumerate(dirs):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    rh[i] = rhvars[xdir]
    height[xdir] =zvals
    init_trac[i] = initval[xdir]
    pcp[i]=precipvals[xdir]/ (400.*400.)

#coloredplot(dirs,sallupdraft,height,'updraftflux',rh)
#height = {}
#for xdir in dirs:
#    height[xdir]=np.arange(len(allupdraft[xdir])) *5



up = np.zeros(75)
for i,dirname in enumerate(dirs):
    up[i]=allupdraft[dirname]/init_trac[i]


powerlaw = lambda x, amp, index: amp * (x**index)


logx = rh
logy = np.log(up)

setvals = np.argsort(rh)


logx = logx[~np.isnan(logy)]
logy = logy[~np.isnan(logy)]



thresh = np.mean(logy)-(2*np.std(logy))
logx = logx[logy>thresh]
logy = logy[logy>thresh]




plt.subplot(2,1,1)
plt.scatter(rh,up,color=cols)
p = np.poly1d(np.polyfit(rh,up,1))
plt.title('Integrated Tracer Flux at 8 km',size=18)
plt.ylabel('Tracer Flux (/m$^2$)')
ax = plt.gca()
plt.subplot(2,1,2)
plt.scatter(logx,logy,color=cols)
variance = np.var(logy)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(logx,logy)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(logx.min(),logx.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.yaxis.labelpad=20
ax.set_ylabel('ln(Tracer Flux)')
ax.set_xlabel('Low Level RH (%)')
ff=plt.text(.2,.7,'$R^2 = %0.2f$'% Rsqr ,color ='black',size=13,weight='black',transform = ax.transAxes)

plt.savefig('newflux-powerlaw2panel-gt2.png')
plt.clf()

up = up/pcp

plt.scatter(rh,up,color=cols)
p = np.poly1d(np.polyfit(rh,up,1))
variance = np.var(up)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,up)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux Scaled by Precip (#/kg)')
ax.set_xlabel('Low Level RH (%)')
ax.set_title('Integrated Tracer Flux at 8 km')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig('newflux-powerlaw-pcpscaled-gt2.png')
plt.clf()









