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

#all5 = {}
#all8 = {}
#all10 = {}
#
#for xdir in dirs:
#    print xdir
#    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
#    height = getvar(files[0],'z_coords')
#    files = sorted(glob.glob('/nobackup/rstorer/code/revu-'+xdir+'*w*h5'))
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
#np.savez('wvals5km-smoothed3km.npz',**all5)
#np.savez('wvals8km-smoothed3km.npz',**all8)
#np.savez('wvals10km-smoothed3km.npz',**all10)

all5 = np.load('tmp/wvals5km-smoothed3km.npz')
all8 = np.load('tmp/wvals8km-smoothed3km.npz')
all10 = np.load('tmp/wvals10km-smoothed3km.npz')

model5 = np.load('tmp/wvals5km.npz')
model8 = np.load('tmp/wvals8km.npz')
model10 = np.load('tmp/wvals10km.npz')

w5k = []
w8k = []
w10k = []

m5k = []
m8k = []
m10k = []

for xdir in dirs:
    w5k.extend(all5[xdir])
    w8k.extend(all8[xdir])
    w10k.extend(all10[xdir])
    m5k.extend(model5[xdir])
    m8k.extend(model8[xdir])
    m10k.extend(model10[xdir])

w5k= np.asarray(w5k)#*-1.
w8k = np.asarray(w8k)#*-1.
w10k = np.asarray(w10k)#*-1.
m5k = np.asarray(m5k)#*-1.
m8k = np.asarray(m8k)#*-1.
m10k = np.asarray(m10k)#*-1.

w5k = w5k[w5k>1]
w8k = w8k[w8k>1]
w10k = w10k[w10k>1]
m5k = m5k[m5k>1]
m8k = m8k[m8k>1]
m10k = m10k[m10k>1]

print len(w5k), len(m5k)
print len(w8k), len(m8k)
print len(w10k), len(m10k)

#plt.hist(w5k,normed=True,bins=100,cumulative=True)
#plt.savefig('hist5km-cum-smoothed3km-updraft.png')
#plt.clf()

#plt.hist(w8k,normed=True,bins=100,cumulative=True)
#plt.savefig('hist8km-cum-smoothed3km-updraft.png')
#plt.clf()

#plt.hist(w10k,normed=True,bins=100,cumulative=True)
#plt.savefig('hist10km-cum-smoothed3km-updraft.png')
#plt.clf()

x1,y1=makecdf(w5k,'cdfw5km-smoothed3km-updraft.png')
x2,y2=makecdf(w8k,'cdfw8km-smoothed3km-updraft.png')
x3,y3=makecdf(w10k,'cdfw10km-smoothed3km-updraft.png')

x4,y4=makecdf(m5k,'cdfw5km-modelres-updraft.png')
x5,y5=makecdf(m8k,'cdfw8km-modelres-updraft.png')
x6,y6=makecdf(m10k,'cdfw10km-modelres-updraft.png')


plt.plot(x1,y1)
plt.plot(x2,y2)
plt.plot(x3,y3)
plt.plot(x4,y4)
plt.plot(x5,y5)
plt.plot(x6,y6)
plt.savefig('cdf6-updraft.png')
plt.clf()
#fig,ax = plt.subplots(1,1)
#w, h = plt.figaspect(.5)
#fig = plt.figure(figsize=(w,h))
fix,axes = plt.subplots(nrows=2,ncols=1)
ax1=axes[1]
ax1.plot(x1,y1,label = '5 km',linewidth=2)
ax1.plot(x2,y2,label = '8 km',linewidth=2)
ax1.plot(x3,y3,label = '10 km',linewidth=2)
ax1.axvline(x=2,color='black')
ax1.axvline(x=2.66,color='black')
ax1.axvline(x=8,color='black')
#ax.set_aspect('.85')
ax1.legend(loc = 'lower right',prop=dict(weight='bold'))
ax1.set_title('Averaged to 3km resolution',fontweight='bold')
#ax1.set_xlim([0,20])
#ax1.set_ylim([0,1.2])
ax1.set_ylabel('Count')
ax1.set_xlabel('m/s')


ax2=axes[0]
ax2.plot(x4,y4,label = '5 km',linewidth=2)
ax2.plot(x5,y5,label = '8 km',linewidth=2)
ax2.plot(x6,y6,label = '10 km',linewidth=2)
ax2.axvline(x=2,color='black')
ax2.axvline(x=2.66,color='black')
ax2.axvline(x=8,color='black')
ax2.legend(loc = 'lower right',prop=dict(weight='bold'))
ax2.set_title('250m resolution',fontweight='bold')
#ax2.set_xlim([0,20])
#ax2.set_ylim([0,1.2])
ax2.set_ylabel('Count')
#ax2.set_xlabel('m/s')


#plt.suptitle('CDF w > 1 m/s', size=18)
plt.tight_layout()
plt.savefig('wcdf-compare-updraft.png')
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
#plt.xlim([0,20])
#plt.ylim([0,1.2])
plt.ylabel('Count')
plt.xlabel('m/s')
plt.savefig('wcdf-3kmres-updraft.png')
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
#plt.xlim([0,20])
#plt.ylim([0,1.2])
plt.ylabel('Count')
plt.xlabel('m/s')
plt.savefig('wcdf-250mres-updraft.png')
plt.clf()











