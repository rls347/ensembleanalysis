import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.colors import LogNorm
from rachelutils.dumbnaming import pert75,case25

def smoothedvar(var):
    smoothvar = np.zeros((82,33,33))-40
    var[var<-40] = -40
    for h in range(82):
        for i in range(6,402,12):
            iind = (i-6)/12
            for j in range(6,402,12):
                jind = (j-6)/12
                smoothvar[h,iind,jind] = np.mean(var[h,i-6:i+6,j-6:j+6])
    return smoothvar

def getmax(var, z):
    height5km = np.argmin(np.abs(z-5000))
    maxvar = np.max(var[height5km:,:,:],0)
    return maxvar

dirs = pert75()
dirs = ['aug17-control','feb23-control','aug11-control']

onebigw = []
onebigdel = []

times = ['mature','growing']
allmodeldirs = case25()
for casenum,case in enumerate(dirs):
    modeldirs = allmodeldirs[casenum]
    for time in times:
        outw = np.load(time+'maxw-3kmavg.npz')
        outdel = np.load(time+'maxdelz-3kmavg.npz')
        allw = []
        alldel = []
        for xdir in dirs:
            w = outw[xdir]
            delz = outdel[xdir]
#            delz = delz[w>5]
#            w=w[w>5]
            if len(w) > 2:
                plt.scatter(w,delz)
            allw.extend(w)
            alldel.extend(delz)
            onebigw.extend(w)
            onebigdel.extend(delz)

        plt.title('3km Footprint, 90s Separation')
        plt.xlabel('Max W (m/s)')
        plt.ylabel('Max dZ/dt (dBZ/min)')
        plt.savefig(case+time+'scatter.png')

        plt.clf()
        allw = np.asarray(allw)
        alldel = np.asarray(alldel)
        print allw.max(), allw.min()
        plt.hist2d(allw,alldel,bins=100,norm=LogNorm())
        plt.xlabel('Max W (m/s)')
        plt.ylabel('Max dZ/dt (dBZ/min)')
        plt.savefig(case+time+'wdelzheatmap.png')
        plt.clf()

xd = np.asarray(onebigw)
yd = np.asarray(onebigdel)

plt.scatter(xd, yd, s=30, alpha=0.15, marker='o')
par = np.polyfit(xd, yd, 1, full=True)

slope=par[0][0]
intercept=par[0][1]
xl = [min(xd), max(xd)]
yl = [slope*xx + intercept  for xx in xl]

# coefficient of determination, plot text
variance = np.var(yd)
residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
Rsqr = np.round(1-residuals/variance, decimals=2)
plt.text(20,20,'$R^2 = %0.2f$'% Rsqr)
plt.plot(xl, yl, '-r',linewidth=2)
plt.xlabel("Max Vertical Velocity (m/s)")
plt.ylabel("Max Reflectivity Difference (dbz/min)")
plt.savefig('allscatterwdelz.png')
plt.clf()

plt.hist2d(xd,yd,bins=100,norm=LogNorm())
plt.text(20,20,'$R^2 = %0.2f$'% Rsqr)
plt.plot(xl, yl, '-r',linewidth=2)
plt.xlabel("Max Vertical Velocity (m/s)")
plt.ylabel("Max Reflectivity Difference (dbz/min)")
plt.savefig('allscatterwdelz-heatmap.png')
plt.clf()




