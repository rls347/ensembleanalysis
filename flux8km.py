import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import glob
from rachelutils.hdfload import getvar
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

sallupdraft = np.load('../filesnpz/budget-timeseries-updrafttracer2flux.npz')
allupdraft = makesum(sallupdraft)

modeldirs = pert75()
height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')
h8 = np.argmin(np.abs(height-8000.0))

oldts = np.zeros((6,75))
newts = np.zeros((6,75))


for t in range(2,7):
    totalflux = {}
    varname = 'tracer00'+str(t)
    area1 = np.load('tracer00'+str(t)+'-updraftflux-w8kmgt1-updraftarea.npz')
    flux1 = np.load('tracer00'+str(t)+'-updraftflux-w8kmgt1.npz')
    area5 = np.load('tracer00'+str(t)+'-updraftflux-wgt5-updraftarea.npz')
    flux5 = np.load('tracer00'+str(t)+'-updraftflux-wgt5.npz')
    newvar = np.load(varname+'_total8kmflux_number.npz')

    for m,xdir in enumerate(modeldirs):
        print xdir, varname
        a1 = area1[xdir]
        a5 = area5[xdir]
        f1 = flux1[xdir]
        f5 = flux5[xdir]

        t1 = a1*f1[h8,:]
        t5 = a5*f5[h8,:]
        t1=t1[f1[h8,:]>0]
        t5=t5[f5[h8,:]>0]

        tot1 = np.sum(t1)*300*250*250
        tot5 = np.sum(t5)*300*250*250

        old = allupdraft[xdir][-1]
        new = newvar[xdir]
        print old, new, old/new
        oldts[t-2,m]=old
        newts[t-2,m]=new

#        files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/trac*h5'))
#        wfiles = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'*h5*'))
#        newtot = 0.
#        for i in range(len(files)):
#            tt = getvar(files[i],varname)[h8,:,:] * (100.**3)
#            ww = getvar(wfiles[i],'w')[h8,:,:]
#            tw = np.sum(tt*ww*250*250*300)
#            newtot = newtot + tw
#        totalflux[xdir]=newtot
#
#    np.savez(varname+'_total8kmflux_number.npz',**totalflux)

colors = ['blue','red','orange','black','green','purple']

for i in range(6):
    plt.scatter(oldts[i,:],newts[i,:],color=colors[i])
plt.savefig('tracerscattertest.png')
plt.clf()
