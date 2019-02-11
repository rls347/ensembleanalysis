import numpy as np
import h5py as hdf
import glob
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75

def budgetplot(maindir, xdir, dx, dy, dt):
	files = sorted(glob.glob(maindir+xdir+'/*.h5'))
	nt = len(files)
	netvert = np.zeros(nt)  
	detrain = np.zeros(nt)  
	advect = np.zeros(nt)  
	totalmicro = np.zeros(nt)  
	pcp = np.zeros(nt)
	updraft = np.zeros(nt)
	totalmass= np.zeros(nt)
	for t, filename in enumerate(files):
		f = hdf.File(filename, 'r')
		w = np.squeeze(f['w'].value)
		rho = (100.* np.squeeze(f['press'].value))/(287.* np.squeeze(f['tempk'].value))
		q =  (np.squeeze(f['total_cond'].value) ) / 1000.
		microdiff = (np.squeeze(f['nuccldrt'].value + f['nucicert'].value + f['vapliqt'].value + f['vapicet'].value)) / 1000. 
		precip = np.squeeze(f['precip3d'].value)
		height = np.squeeze(f['z_coords'].value)
		f.close()
		dz = np.zeros_like(height)
		dz[:-1] = np.diff(height)
		dz[-1] = dz[-2]
		qdz = q*dz[:,None,None]
		nz = q.shape[0]
		nx = q.shape[1]
		ny = q.shape[2]
		azz = np.argmin(np.absolute(height-8000))
		bzz = nz-1
		axx = 1#180 - (10000/dx)
		bxx = 399#180 + (10000/dx)
		ayy = 1#240 - (10000/dy)
		byy = 399#240 + (10000/dy)

		advw = rho * w * q
        
		pcp[t] = (dx * dy * dt * (np.sum(precip[azz,axx:bxx,ayy:byy])-np.sum(precip[bzz,axx:bxx,ayy:byy])))*-1
		updraft[t] = (dx * dy * dt * (np.sum(advw[azz,axx:bxx,ayy:byy])-np.sum(advw[bzz,axx:bxx,ayy:byy])))
		netvert[t] = updraft[t] + pcp[t] 
		totalmass[t]  = np.sum(q[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy] *dz[azz:bzz,None,None]) * dx * dy	
		totalmicro[t] = np.sum(microdiff[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
        
	factor = 1.e7
	print 'updraft: ', np.sum(updraft)/factor
	print 'micro: ', np.sum(totalmicro)/factor
	print 'precip: ', np.sum(pcp)/factor
	print 'net vertical: ', np.sum(netvert)/factor
	print 'total mass: ',totalmass[-1]/factor
	print (np.sum(totalmicro) + np.sum(netvert))/factor
	print ' '
	allupdrafts = np.sum(updraft)/factor
	allmicro= np.sum(totalmicro)/factor
	allprecip= np.sum(pcp)/factor
	allvertical= np.sum(netvert)/factor
	allmass= totalmass[-1]/factor
	return allupdrafts,allmicro,allprecip,allvertical,allmass


allupdrafts = {}
allmicro = {}
allprecip = {}
allvertical = {}
allmass = {}

    
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = pert75()
dx = 250
dy = 250
dt = 300
for xdir in modeldirs:
	print xdir
	allupdrafts[xdir],allmicro[xdir],allprecip[xdir],allvertical[xdir],allmass[xdir] = budgetplot(maindir, xdir, dx, dy, dt)


np.savez('budgetintegral-revu-updraft.npz',**allupdrafts)
np.savez('budgetintegral-revu-micro.npz',**allmicro)
np.savez('budgetintegral-revu-precip.npz',**allprecip)
np.savez('budgetintegral-revu-vertical.npz',**allvertical)
np.savez('budgetintegral-revu-endmass.npz',**allmass)


