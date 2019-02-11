import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar

#helpful cdf code copied from stack overflow
def makecdf(data,outname):

    data_size=len(data)
    print data.shape
    print data_size
    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    x = bin_edges[0:-1]
    y = cdf

    f = interp1d(x, y)
#    f2 = interp1d(x, y, kind='cubic')
    xnew = np.linspace(0, max(x), num=1000, endpoint=True)

    # Plot the cdf
#    plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
    plt.plot(x,y)
    plt.legend(['data', 'linear', 'cubic'], loc='best')
    plt.title("Interpolation")
    plt.ylim((0,1))
    plt.ylabel("CDF")
    plt.grid(True)
    plt.savefig(outname)
    plt.clf()

    return x,y

dirs = pert75()
all5 = {}
all8 = {}
all10 = {}

#for xdir in dirs:
#    print xdir
#    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
#    height = getvar(files[0],'z_coords')
#    files = sorted(glob.glob('/nobackup/rstorer/h5files/revu-'+xdir+'*vap*h5'))
#    print len(files)
#    z5 = np.argmin(abs(height-5000.))
#    z8 = np.argmin(abs(height-8000.))
#    z10 = np.argmin(abs(height-10000.))
#
#    w5 = []
#    w8 = []
#    w10 = []
#
#    for fil in files:
#        w = getvar(fil,'q')
#        ww5 = w[z5,:,:]
#        ww8 = w[z8,:,:]
#        ww10 = w[z10,:,:]
#        maxw = np.max(w,0)
#
#        w5.extend(ww5)
#        w8.extend(ww8)
#        w10.extend(ww10)
#
#    all5[xdir] =np.asarray(w5)
#    all8[xdir] = np.asarray(w8)
#    all10[xdir] = np.asarray(w10)
#
#np.savez('tmp/vaporvals5km-smoothed3km.npz',**all5)
#np.savez('tmp/vaporvals8km-smoothed3km.npz',**all8)
#np.savez('tmp/vaporvals10km-smoothed3km.npz',**all10)

wall5 = np.load('tmp/wvals5km-smoothed3km.npz')
wall8 = np.load('tmp/wvals8km-smoothed3km.npz')
wall10 = np.load('tmp/wvals10km-smoothed3km.npz')

wmodel5 = np.load('tmp/wvals5km.npz')
wmodel8 = np.load('tmp/wvals8km.npz')
wmodel10 = np.load('tmp/wvals10km.npz')

w5k = []
w8k = []
w10k = []

wm5k = []
wm8k = []
wm10k = []

rhoall5 = np.load('tmp/rhovals5km-smoothed3km.npz')
rhoall8 = np.load('tmp/rhovals8km-smoothed3km.npz')
rhoall10 = np.load('tmp/rhovals10km-smoothed3km.npz')

rhomodel5 = np.load('tmp/rhovals5km.npz')
rhomodel8 = np.load('tmp/rhovals8km.npz')
rhomodel10 = np.load('tmp/rhovals10km.npz')

rho5k = []
rho8k = []
rho10k = []

rhom5k = []
rhom8k = []
rhom10k = []

vaporall5 = np.load('tmp/vaporvals5km-smoothed3km.npz')
vaporall8 = np.load('tmp/vaporvals8km-smoothed3km.npz')
vaporall10 = np.load('tmp/vaporvals10km-smoothed3km.npz')

vapormodel5 = np.load('tmp/vaporvals5km.npz')
vapormodel8 = np.load('tmp/vaporvals8km.npz')
vapormodel10 = np.load('tmp/vaporvals10km.npz')

vapor5k = []
vapor8k = []
vapor10k = []

vaporm5k = []
vaporm8k = []
vaporm10k = []


for xdir in dirs:
    w5k.extend(wall5[xdir])
    w8k.extend(wall8[xdir])
    w10k.extend(wall10[xdir])
    wm5k.extend(wmodel5[xdir])
    wm8k.extend(wmodel8[xdir])
    wm10k.extend(wmodel10[xdir])
    vapor5k.extend(vaporall5[xdir])
    vapor8k.extend(vaporall8[xdir])
    vapor10k.extend(vaporall10[xdir])
    vaporm5k.extend(vapormodel5[xdir])
    vaporm8k.extend(vapormodel8[xdir])
    vaporm10k.extend(vapormodel10[xdir])
    rho5k.extend(rhoall5[xdir])
    rho8k.extend(rhoall8[xdir])
    rho10k.extend(rhoall10[xdir])
    rhom5k.extend(rhomodel5[xdir])
    rhom8k.extend(rhomodel8[xdir])
    rhom10k.extend(rhomodel10[xdir])

w5k= np.asarray(w5k)
w8k = np.asarray(w8k)
w10k = np.asarray(w10k)
wm5k = np.asarray(wm5k)
wm8k = np.asarray(wm8k)
wm10k = np.asarray(wm10k)
print w5k.shape, wm5k.shape

vapor5k= np.asarray(vapor5k)
vapor8k = np.asarray(vapor8k)
vapor10k = np.asarray(vapor10k)
vaporm5k = np.asarray(vaporm5k)
vaporm8k = np.asarray(vaporm8k)
vaporm10k = np.asarray(vaporm10k)
print vapor5k.shape,vaporm5k.shape

rho5k= np.asarray(rho5k)
rho8k = np.asarray(rho8k)
rho10k = np.asarray(rho10k)
rhom5k = np.asarray(rhom5k)
rhom8k = np.asarray(rhom8k)
rhom10k = np.asarray(rhom10k)
print rho5k.shape, rhom5k.shape



vapor5k = vapor5k[w5k>1]
vapor8k = vapor8k[w8k>1]
vapor10k = vapor10k[w10k>1]
vaporm5k = vaporm5k[wm5k>1]
vaporm8k = vaporm8k[wm8k>1]
vaporm10k = vaporm10k[wm10k>1]

rho5k = rho5k[w5k>1]
rho8k = rho8k[w8k>1]
rho10k = rho10k[w10k>1]
rhom5k = rhom5k[wm5k>1]
rhom8k = rhom8k[wm8k>1]
rhom10k = rhom10k[wm10k>1]

w5k = w5k[w5k>1]
w8k = w8k[w8k>1]
w10k = w10k[w10k>1]
wm5k = wm5k[wm5k>1]
wm8k = wm8k[wm8k>1]
wm10k = wm10k[wm10k>1]

print rho5k.shape, w5k.shape,vapor5k.shape

w5k = w5k*rho5k*vapor5k*1000.
w8k = w8k*rho8k*vapor8k*1000.
w10k = w10k*rho10k*vapor10k*1000.
wm5k = wm5k*rhom5k*vaporm5k*1000.
wm8k = wm8k*rhom8k*vaporm8k*1000.
wm10k = wm10k*rhom10k*vaporm10k*1000.




print len(w5k), len(wm5k)
print len(w8k), len(wm8k)
print len(w10k), len(wm10k)

plt.hist(w5k,normed=True,bins=100,cumulative=True)
plt.savefig('hist5km-cum-smoothed3km-vapormassflux.png')
plt.clf()

plt.hist(w8k,normed=True,bins=100,cumulative=True)
plt.savefig('hist8km-cum-smoothed3km-vapormassflux.png')
plt.clf()

plt.hist(w10k,normed=True,bins=100,cumulative=True)
plt.savefig('hist10km-cum-smoothed3km-vapormassflux.png')
plt.clf()

x1,y1=makecdf(w5k,'cdfw5km-smoothed3km-vapormassflux.png')
x2,y2=makecdf(w8k,'cdfw8km-smoothed3km-vapormassflux.png')
x3,y3=makecdf(w10k,'cdfw10km-smoothed3km-vapormassflux.png')

x4,y4=makecdf(wm5k,'cdfw5km-modelres-vapormassflux.png')
x5,y5=makecdf(wm8k,'cdfw8km-modelres-vapormassflux.png')
x6,y6=makecdf(wm10k,'cdfw10km-modelres-vapormassflux.png')


plt.plot(x1,y1)
plt.plot(x2,y2)
plt.plot(x3,y3)
plt.plot(x4,y4)
plt.plot(x5,y5)
plt.plot(x6,y6)
plt.savefig('cdf6-vapormassflux.png')
plt.clf()
fig,ax = plt.subplots(1,1)
w, h = plt.figaspect(.5)
fig = plt.figure(figsize=(w,h))
fix,axes = plt.subplots(nrows=2,ncols=1)
ax1=axes[1]
ax1.plot(x1,y1,label = '5 km',linewidth=2)
ax1.plot(x2,y2,label = '8 km',linewidth=2)
ax1.plot(x3,y3,label = '10 km',linewidth=2)
ax1.axvline(x=2,color='black')
ax1.axvline(x=2.66,color='black')
ax1.axvline(x=8,color='black')
ax.set_aspect('.85')
ax1.legend(loc = 'lower right',prop=dict(weight='bold'))
ax1.set_title('Averaged to 3km resolution',fontweight='bold')
ax1.set_xlim([0,20])
ax1.set_ylim([0,1.2])
ax1.set_ylabel('Count')
ax1.set_xlabel('kg/m$^2$s')


ax2=axes[0]
ax2.plot(x4,y4,label = '5 km',linewidth=2)
ax2.plot(x5,y5,label = '8 km',linewidth=2)
ax2.plot(x6,y6,label = '10 km',linewidth=2)
ax2.axvline(x=2,color='black')
ax2.axvline(x=2.66,color='black')
ax2.axvline(x=8,color='black')
ax2.legend(loc = 'lower right',prop=dict(weight='bold'))
ax2.set_title('250m resolution',fontweight='bold')
ax2.set_xlim([0,20])
ax2.set_ylim([0,1.2])
ax2.set_ylabel('Count')
ax2.set_xlabel('kg/m$^2$s')


plt.suptitle('CDF w > 1 m/s', size=18)
plt.tight_layout()
plt.savefig('wcdf-compare-vapormassflux.png')
plt.clf()

fig,ax = plt.subplots(1,1)
w, h = plt.figaspect(.5)
fig = plt.figure(figsize=(w,h))
plt.plot(x1,y1,label = '5 km',linewidth=2)
plt.plot(x2,y2,label = '8 km',linewidth=2)
plt.plot(x3,y3,label = '10 km',linewidth=2)
plt.axvline(x=2)
plt.axvline(x=2.66)
plt.axvline(x=8)
plt.legend(loc = 'lower right',prop=dict(weight='bold'))
plt.title('Averaged to 3km resolution',fontweight='bold')
plt.xlim([0,20])
plt.ylim([0,1.2])
plt.ylabel('Count')
plt.xlabel('kg/m$^2$s')
plt.savefig('wcdf-3kmres-vapormassflux.png')
plt.clf()


fig,ax = plt.subplots(1,1)
w, h = plt.figaspect(.5)
fig = plt.figure(figsize=(w,h))
plt.plot(x4,y4,label = '5 km',linewidth=2)
plt.plot(x5,y5,label = '8 km',linewidth=2)
plt.plot(x6,y6,label = '10 km',linewidth=2)
plt.axvline(x=2)
plt.axvline(x=2.66)
plt.axvline(x=8)
plt.legend(loc = 'lower right',prop=dict(weight='bold'))
plt.title('250m resolution',fontweight='bold')
plt.xlim([0,20])
plt.ylim([0,1.2])
plt.ylabel('Count')
plt.xlabel('kg/m$^2$s')
plt.savefig('wcdf-250mres-vapormassflux.png')
plt.clf()











