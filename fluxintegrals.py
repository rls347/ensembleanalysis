import numpy as np
import h5py as hdf
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
    vapflux = np.zeros(nt)
    tracflux = np.zeros(nt)
    totalmass= np.zeros(nt)
    for t,filename in enumerate(files):
        print t
        f = hdf.File(filename,'r')
        w = getvar(f,'w')
        q = getvar(f,'total_cond') / 1000.
        vap = getvar(f,'vapor')/1000.
        trac = getvar(f,'tracer002') * (100.**3)
        height = getvar(f, 'z_coords')
        rho = getrho(f)
        dz = getdz(f)
        f.close()
        nz,nx,ny = q.shape
        azz = np.argmin(np.absolute(height-8000))
        bzz = nz-1

        advw = rho * w * q
        advv = rho * w * vap
        advt = w * trac

        updraft[t] = dx * dy * dt * (np.sum(advw[azz,:,:]) - np.sum(advw[bzz,:,:]))
        vapflux[t] = dx * dy * dt * (np.sum(advv[azz,:,:]) - np.sum(advv[bzz,:,:]))
        tracflux[t] = dx * dy * dt * (np.sum(advt[azz,:,:]) - np.sum(advt[bzz,:,:]))
        totalmass[t] = np.sum(q[azz:bzz,:,:]*rho[azz:bzz,:,:] * dz[azz:bzz,None,None]) * dx * dy




    for t,filename in enumerate(files):
        print t
 #       advw = rho * w * q
 #       advv = rho * w * vap
 #       advt = w * trac

#        updraft[t] = dx * dy * dt * (np.sum(advw[azz,:,:]) - np.sum(advw[bzz,:,:]))
#        vapflux[t] = dx * dy * dt * (np.sum(advv[azz,:,:]) - np.sum(advv[bzz,:,:]))
#        tracflux[t] = dx * dy * dt * (np.sum(advt[azz,:,:]) - np.sum(advt[bzz,:,:]))
#        totalmass[t] = np.sum(q[azz:bzz,:,:]*rho[azz:bzz,:,:] * dz[azz:bzz,None,None]) * dx * dy

	return updraft, vapflux, tracflux, totalmass 


allupdrafts = {}
allvapflux = {}
alltracflux = {}
allmass = {}

    
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = pert75()
dx = 250
dy = 250
dt = 300
for xdir in modeldirs:
	print xdir
	allupdrafts[xdir],allvapflux[xdir],alltracflux[xdir],allmass[xdir] = budgetplot(maindir, xdir, dx, dy, dt)


np.savez('budget-timeseries-updraftcondflux.npz',**allupdrafts)
np.savez('budget-timeseries-updraftvaporflux.npz',**allvapflux)
np.savez('budget-timeseries-updrafttracer2flux.npz',**alltracflux)
np.savez('budget-timeseries-totalmass.npz',**allmass)


