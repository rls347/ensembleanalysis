import numpy as np
import h5py as hdf
import copy
import glob
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar, getdz, getrho

def budgetplot(maindir, xdir, dx, dy, dt):
    files = sorted(glob.glob(maindir+xdir+'/*.h5'))
    nt = len(files)
    updraft = np.zeros(nt)
    onlyup = np.zeros(nt)
    for t,filename in enumerate(files):
        print t
        f = hdf.File(filename,'r')
        w = getvar(f,'w')
        height = getvar(f, 'z_coords')
        rho = getrho(f)
        dz = getdz(f)
        f.close()
        nz,nx,ny = w.shape
        azz = np.argmin(np.absolute(height-8000))
        bzz = nz-1
        advw = rho * w
        upw = copy.deepcopy(advw)
        upw[w<1]=0.
        updraft[t] = dx * dy * dt * (np.sum(advw[azz,:,:]) - np.sum(advw[bzz,:,:]))
        onlyup[t] = dx * dy * dt * (np.sum(upw[azz,:,:]) - np.sum(upw[bzz,:,:]))
    return updraft,onlyup


allupdrafts = {}
gt1up = {}

    
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = pert75()
dx = 250
dy = 250
dt = 300
for xdir in modeldirs:
	print xdir
	allupdrafts[xdir],gt1up[xdir] = budgetplot(maindir, xdir, dx, dy, dt)


np.savez('budget-timeseries-dryairmassflux.npz',**allupdrafts)
np.savez('budget-timeseries-dryairmassflux-wgt1.npz',**gt1up)



