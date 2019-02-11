import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75

    
def multifig(xdir, z2, height, varname, dirout):
    var = np.asarray(z2)
    if var.max() >0 or var.min() <0:
        nx = var.shape[2]
        xs = np.linspace(0.,100.,nx*1.0)
        levels = np.linspace(var.min(), var.max(), 20)
        #levels = np.logspace(-2,3, 20)
        
        fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

        for t in range(16):
            try:
                ax = axes.flat[t]
                f = ax.contourf(xs, height, z2[t], levels = levels)
                if height.max() > 20000:
                    plt.ylim(0,17000)
            except:
                print 'time ', t, 'has no value in ', xdir
        cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(f, cax=cax, **kw)
        plt.savefig(dirout+xdir+'.'+varname+'.timeseriespics-sum.png')
        plt.close()

def slicetracer(maindir, modeldirs, dirout, varname, timediff):
    print varname
    for xdir in modeldirs:
        try:
            filesrams = sorted(glob.glob(maindir+xdir+"/tr*h5"))
            numfiles = len(filesrams)
            print numfiles
            z2 = []
            for time in range(0,numfiles,timediff):
                rfile = hdf.File(filesrams[time], "r")
                var = np.squeeze(rfile[varname].value)
                height = np.squeeze(rfile['z_coords'].value)
                ny = var.shape[2]
                #z2.append(var[:,ny/2,:])
                v = np.sum(var,1)
                z2.append(v)
                rfile = hdf.File(filesrams[0], "r")
                height = np.squeeze(rfile['z_coords'].value)

            print len(z2)    
            multifig(xdir, z2, height, varname, dirout)
        except:
            print 'no bueno', xdir


########################################

maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = pert75()

#slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer001', 3)
slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer002', 3)
slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer004', 3)
slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer003', 3)
slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer005', 3)
slicetracer(maindir, modeldirs, '/nobackup/rstorer/plots/tracerplot-','tracer006', 3)

