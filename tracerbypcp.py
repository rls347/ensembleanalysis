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

dirs = pert75()
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')


initval = {}
profs = {}
for i, dirname in enumerate(dirs):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))
#    outdir = '/nobackup/rstorer/plots/'
    outdir = './'
    nt = len(files)
    t2 = getvar(files[0],'tracer002')[:,100,100]
    dz = getdz(files[0])
    x = t2*dz*100*100*100
    initval[dirname]=np.sum(x)
    profs[dirname]=t2


sallupdraft = np.load('../filesnpz/budget-timeseries-updrafttracer2flux.npz')
allupdraft = makesum(sallupdraft)
height = getvar(files[0],'z_coords')/1000.
#allrh = np.load('../filesnpz/init_vertintvap.npz')
allrh = np.load('../filesnpz/rhlow.npz')
precipvals= np.load('../filesnpz/totpcpmm.npz')
rh = np.zeros(75)
pcp = np.zeros(75)
init_trac = np.zeros(75)
for i,xdir in enumerate(dirs):
    rh[i]=allrh[xdir]
    init_trac[i] = initval[xdir]
    pcp[i]=precipvals[xdir]/(400.*400.)



up = np.zeros(75)
updiv = np.zeros(75)
for i,dirname in enumerate(dirs):
    up[i]=allupdraft[dirname][-1]
    updiv[i]=up[i]/pcp[i]


plt.scatter(rh,up,color=cols)
p = np.poly1d(np.polyfit(rh,up,2))
variance = np.var(up)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,up)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux')
#ax.set_xlabel('High Level RH (%)')
ax.set_xlabel('rhlow')
#ax.set_xlabel('Column Water Vapor (mm)')
ax.set_title('Integrated Tracer Flux at 8 km')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-nodiv-rhlow-oldcode.png')
plt.clf()


plt.scatter(rh,updiv,color=cols)
p = np.poly1d(np.polyfit(rh,updiv,2))
variance = np.var(updiv)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,updiv)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux/Precip')
ax.set_xlabel('High Level RH (%)')
ax.set_xlabel('rhlow')
#ax.set_xlabel('Column Water Vapor (mm)')
ax.set_title('Integrated Tracer Flux at 8 km/total precip')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-rhlow-oldcode.png')
plt.clf()



plt.scatter(rh,pcp,color=cols)
p = np.poly1d(np.polyfit(rh,pcp,2))
variance = np.var(pcp)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,pcp)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(rh.min(),rh.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Precip')
ax.set_xlabel('High Level RH (%)')
ax.set_xlabel('rhlow')
#ax.set_xlabel('Column Water Vapor (mm)')
ax.set_title('column water vs total precip')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-totprecipvsrhlow-oldcode.png')
plt.clf()



plt.scatter(up,updiv,color=cols)
p = np.poly1d(np.polyfit(up,updiv,2))
variance = np.var(updiv)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(up,updiv)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(up.min(),up.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux/Precip')
ax.set_xlabel('Tracer Flux')
ax.set_title('Integrated Tracer Flux at 8 km/total precip')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-upvsupdiv-rhlow-oldcode.png')
plt.clf()



plt.scatter(pcp,updiv,color=cols)
p = np.poly1d(np.polyfit(pcp,updiv,2))
variance = np.var(updiv)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(pcp,updiv)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(pcp.min(),pcp.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux/Precip')
ax.set_xlabel('precip')
ax.set_title('Integrated Tracer Flux at 8 km/total precip')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-pcpvsupdiv-rhlow-oldcode.png')
plt.clf()



plt.scatter(pcp,up,color=cols)
p = np.poly1d(np.polyfit(pcp,up,2))
variance = np.var(up)
residuals = np.var([(p(xx)-yy) for xx, yy in zip(pcp,up)])
Rsqr = np.round(1-residuals/variance, decimals=2)
xp = np.linspace(pcp.min(),pcp.max(),100)
plt.plot(xp,p(xp))
ax = plt.gca()
ax.set_ylabel('Tracer Flux')
ax.set_xlabel('precip')
#ax.set_title('Integrated Tracer Flux at 8 km/total precip')
plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
plt.savefig(outdir+'/scatterfluxbypcp-pcpvsup-rhlow-oldcode.png')
plt.clf()

