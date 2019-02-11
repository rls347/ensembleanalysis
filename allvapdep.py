import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import numpy as np
import h5py as hdf
import glob


def plotstuff(xs, ys, labelname, xlab, ylab, outname,xpos,ypos):
    xd = xs
    yd = ys
    par = np.polyfit(xd, yd, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    xl = [min(xd), max(xd)]
    yl = [slope*xx + intercept  for xx in xl]

    variance = np.var(yd)
    residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
    Rsqr = np.round(1-residuals/variance, decimals=2)

    return xl,yl,Rsqr,slope

def modelvars(filename,arg):
    fil = hdf.File(filename,'r')
    vapdep= (getvar(fil, 'vapicet')[arg:,:,:]+getvar(fil,'vapliqt')[arg:,:,:])*2
    temp= getvar(fil, 'tempk')[arg:,10,10]
    w = getvar(fil, 'w')[arg:,:,:]
    fil.close()
    return vapdep,w,temp

alldirs = pert75()
#alldirs = ['aug17-control','feb23-control','aug11-control']
height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')
h5km = np.argmin(np.abs(height-5000.))
minarray = np.arange(-80,0,5)+273.15

alphavals = {}
rvals = {}


for xdir in alldirs:
    alphavals[xdir] = np.zeros_like(minarray)
    rvals[xdir]=np.zeros_like(minarray)
    outgraup= []
    outw = []
    for i in range(len(minarray)):
        outgraup.append([])
        outw.append([])
    files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/'+xdir+'/*h5'))
    nt = len(files)    
    for t in range(1,nt):
        print xdir, t
        vapdep,w,temp = modelvars(files[t],h5km)
        for tval, num in enumerate(minarray):
            tempmin = num
            tempmax = num+5

            cold = np.where(np.logical_and(temp>tempmin,temp<tempmax))

            cgraup = vapdep[cold,:,:]
            cw = w[cold,:,:]
    
            cg = cgraup[cw>1]
            ww = cw[cw>1]

            outgraup[tval].extend(cg)
            outw[tval].extend(ww)

    for tval,num in enumerate(minarray):
        tempmin = num
        w = np.asarray(outw[tval])
        allvap= np.asarray(outgraup[tval])
        try:
            xl,yl,Rsqr,slope = plotstuff(w, allvap, 'sum', 'w (m/s)', 'Updrafts','dummyfile.png',.4,.83)

            alphavals[xdir][tval]=slope
            rvals[xdir][tval]=Rsqr
        except:
            print 'no values in: ', minarray

xdir='aug11-control'
plt.plot(minarray,alphavals[xdir],label = 'August 11',color='blue',marker='o')
plt.plot(minarray,alphavals[xdir],color='blue',linewidth=2)
for i in range(1,25):
    xdir = alldirs[i]
    plt.plot(minarray,alphavals[xdir],color='blue',marker='o')
    plt.plot(minarray,alphavals[xdir],color='blue',linewidth=2)

xdir = 'aug17-control'
plt.plot(minarray,alphavals[xdir],label = 'August 17',color='orange',marker='o')
plt.plot(minarray,alphavals[xdir],color='orange',linewidth=2)
for i in range(26,50):
    xdir = alldirs[i]
    plt.plot(minarray,alphavals[xdir],color='orange',marker='o')
    plt.plot(minarray,alphavals[xdir],color='orange',linewidth=2)

xdir='feb23-control'
plt.plot(minarray,alphavals[xdir],label = 'Feb 23',color='purple',marker='o')
plt.plot(minarray,alphavals[xdir],color='purple',linewidth=2)
for i in range(51,75):
    xdir = alldirs[i]
    plt.plot(minarray,alphavals[xdir],color='purple',marker='o')
    plt.plot(minarray,alphavals[xdir],color='purple',linewidth=2)

plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Alpha')
plt.title('Updrafts',size=16)
plt.savefig('alphacurves-updraft-vapdep.png')
plt.clf()


xdir='aug11-control'
plt.plot(minarray,rvals[xdir],label = 'August 11',color='blue',marker='o')
plt.plot(minarray,rvals[xdir],color='blue',linewidth=2)
for i in range(1,25):
    xdir = alldirs[i]
    plt.plot(minarray,rvals[xdir],color='blue',marker='o')
    plt.plot(minarray,rvals[xdir],color='blue',linewidth=2)

xdir = 'aug17-control'
plt.plot(minarray,rvals[xdir],label = 'August 17',color='orange',marker='o')
plt.plot(minarray,rvals[xdir],color='orange',linewidth=2)
for i in range(26,50):
    xdir = alldirs[i]
    plt.plot(minarray,rvals[xdir],color='orange',marker='o')
    plt.plot(minarray,rvals[xdir],color='orange',linewidth=2)

xdir='feb23-control'
plt.plot(minarray,rvals[xdir],label = 'Feb 23',color='purple',marker='o')
plt.plot(minarray,rvals[xdir],color='purple',linewidth=2)
for i in range(51,75):
    xdir = alldirs[i]
    plt.plot(minarray,rvals[xdir],color='purple',marker='o')
    plt.plot(minarray,rvals[xdir],color='purple',linewidth=2)



plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Rsqr')
plt.title('Updrafts',size=16)
plt.savefig('rcurves-updraft-vapdep.png')
plt.clf()


xdir='aug11-control'
plt.plot(minarray,rvals[xdir],label = 'August 11',color='blue',marker='o')
plt.plot(minarray,rvals[xdir],color='blue',linewidth=2)

xdir = 'aug17-control'
plt.plot(minarray,rvals[xdir],label = 'August 17',color='orange',marker='o')
plt.plot(minarray,rvals[xdir],color='orange',linewidth=2)

xdir='feb23-control'
plt.plot(minarray,rvals[xdir],label = 'Feb 23',color='purple',marker='o')
plt.plot(minarray,rvals[xdir],color='purple',linewidth=2)

plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Rsqr')
plt.title('Updrafts',size=16)
plt.savefig('rcurves-updraft-controlonly-vapdep.png')
plt.clf()


xdir='aug11-control'
plt.plot(minarray,alphavals[xdir],label = 'August 11',color='blue',marker='o')
plt.plot(minarray,alphavals[xdir],color='blue',linewidth=2)

xdir = 'aug17-control'
plt.plot(minarray,alphavals[xdir],label = 'August 17',color='orange',marker='o')
plt.plot(minarray,alphavals[xdir],color='orange',linewidth=2)

xdir='feb23-control'
plt.plot(minarray,alphavals[xdir],label = 'Feb 23',color='purple',marker='o')
plt.plot(minarray,alphavals[xdir],color='purple',linewidth=2)

plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Rsqr')
plt.title('Updrafts',size=16)
plt.savefig('alphacurves-updraft-controlonly-vapdep.png')
plt.clf()

