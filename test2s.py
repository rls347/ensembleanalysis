import numpy as np
import h5py as hdf
import glob
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pdb
import copy

def budgetplot(maindir, xdir, dx, dy, dt):
	files = sorted(glob.glob(maindir+xdir+'/bas*.h5'))
	nt = len(files)
	print nt
	netvert = np.zeros(nt)  
	detrain = np.zeros(nt)  
	advect = np.zeros(nt)  
	totalmicro = np.zeros(nt)  
	nucliq= np.zeros(nt)
	nucice = np.zeros(nt)
	vapliq = np.zeros(nt)
	vapice = np.zeros(nt)
	totalmass = np.zeros(nt)    
	diffmass = np.zeros(nt)
	pcp = np.zeros(nt)
	updraft = np.zeros(nt)
	condabove8 = np.zeros(nt)
	cloud = np.zeros(nt)
	drizzle = np.zeros(nt)
	rain = np.zeros(nt)
	pristine = np.zeros(nt)
	snow = np.zeros(nt)
	graupel = np.zeros(nt)
	aggregates = np.zeros(nt)
	hail = np.zeros(nt)
	for t, filename in enumerate(files):
		print t, len(files)
		f = hdf.File(filename, 'r')
		w = np.squeeze(f['w'].value)
		u = np.squeeze(f['u'].value)
		v = np.squeeze(f['v'].value)
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
		print azz, azz, azz
		bzz = nz-1
		midx = 200
		midy = 300
		axx = 1#midx - (10000/dx)  #should be 2500 for 5km footprint
		bxx = 398#midx + (10000/dx)
		ayy = 1#midy - (10000/dy)
		byy = 398#midy + (10000/dy)

		micro2d = np.sum(microdiff,1)
		cloud2d = np.sum(q, 1)	
		if t == 0:
			prev = copy.deepcopy(cloud2d)
			print 'ZEROOO'


		meanu = np.mean((np.mean(u,1)),1)
		meanv = np.mean((np.mean(v,1)),1)
		vprime = v - meanv[:,None,None]
		uprime = u - meanu[:,None,None]
		
		rhouqp = rho * uprime * q
		rhovqp = rho * vprime * q

#		qmid = np.zeros_like(q)
#		for hg in range(nz-1):
#			tmp1 = rho[hg,:,:] * q[hg,:,:]
#			tmp2 = rho[hg+1,:,:] * q[hg+1,:,:]
#			new = (tmp1+tmp2)/2.0
#			qmid[hg,:,:] = np.mean( np.array([ tmp1, tmp2 ]), axis=0 )
		
		advu = rho * meanu[:,None,None] * q
		advv = rho * meanv[:,None,None] * q
		advw = q * w
		w2d = np.sum(advw,1)
		pcp[t] = (dx * dy * dt * (np.sum(precip[azz,axx:bxx,ayy:byy])-np.sum(precip[bzz,axx:bxx,ayy:byy])))*-1
		totalmass[t]  = np.sum(q[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy] *dz[azz:bzz,None,None]) * dx * dy
		updraft[t] = (dx * dy * dt * (np.sum(advw[azz,axx:bxx,ayy:byy])-np.sum(advw[bzz,axx:bxx,ayy:byy])))
		netvert[t] = updraft[t] + pcp[t] 
		
		detrainx = np.zeros(nz)
		detrainy = np.zeros(nz)
		for k in range(nz):
			left = np.sum(rhouqp[k,axx:bxx,ayy]) * dz[k] * dy * dt
			right = np.sum(rhouqp[k,axx:bxx,byy]) * dz[k] * dy * dt
			detrainx[k] = left-right
			
			up = np.sum(rhovqp[k,bxx,ayy:byy]) * dz[k] * dy * dt
			down = np.sum(rhovqp[k,axx, ayy:byy]) * dz[k] * dy * dt
			detrainy[k] = down - up
			
		advectx = np.zeros(nz)
		advecty = np.zeros(nz)
		for k in range(nz):
			leftarray = np.sum(advu[k,axx:bxx,ayy]) * dz[k] * dy * dt
			rightarray = np.sum(advu[k,axx:bxx,byy]) * dz[k] * dy * dt
			advectx[k] = leftarray - rightarray
			uparray = np.sum(advv[k,bxx,ayy:byy]) * dz[k] * dx * dt
			downarray = np.sum(advv[k,axx, ayy:byy]) * dz[k] * dx * dt
			advecty[k] = downarray - uparray
			
		detrain[t] = np.sum(detrainx[azz:bzz]+detrainy[azz:bzz])
		advect[t] = np.sum(advectx[azz:bzz]+advecty[azz:bzz])
		totalmicro[t] = np.sum(microdiff[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
        
		strt = str(t)
		if t<10:
			strt = '0'+strt
		if t<100:
			strt = '0'+strt

		plt.contourf(cloud2d[46:52,200:300])
		plt.colorbar()
		plt.savefig('/nobackup/rstorer/plots/test2s/cloudtot'+strt+'.png')
		plt.clf()

		plt.contourf(w2d[46:52,200:300])
		plt.colorbar()
		plt.savefig('/nobackup/rstorer/plots/test2s/vertadvtot'+strt+'.png')
		plt.clf()

		micro2d = micro2d * 1000.

		plt.contourf(micro2d[46:52,200:300])#,levels = [-2,-1.5,-1,-.5,0,.5,1,1.5,2])
		plt.colorbar()
		plt.savefig('/nobackup/rstorer/plots/test2s/microtot'+strt+'.png')
		plt.clf()

		diff2d = cloud2d-prev
		plt.contourf(diff2d[46:52,200:300])
		plt.colorbar()
		plt.savefig('/nobackup/rstorer/plots/test2s/diffcloudtot'+strt+'.png')
		plt.clf()

		if t>0:
			prev = copy.deepcopy(cloud2d)	



	diffmass[1:] = np.diff(totalmass)   
	xvals = np.arange(nt) * (dt/60.) + 80. 
    
	testtest = netvert + advect  + detrain + totalmicro
	diffdiff = diffmass - testtest

	
	fig,ax = plt.subplots()
	ax.axhline(y=0,linestyle='--',color = 'gray')
	plt.plot(xvals[1:],netvert[1:], color = 'orange', label = 'Vertical Flux', linewidth = 3)
	plt.plot(xvals[1:],updraft[1:], color = 'darkgreen', label = 'updraft Flux', linewidth = 3)
	plt.plot(xvals[1:],pcp[1:], color = 'lightgreen', label = 'precip Flux', linewidth = 3)
	plt.plot(xvals[1:],detrain[1:], color = 'red', label = 'Detrainment', linewidth = 3)
	plt.plot(xvals[1:],advect[1:], color = 'blue', label = 'Advection', linewidth = 3)
	plt.plot(xvals[1:],totalmicro[1:], color = 'purple', label = 'Microphysics', linewidth = 3)
	plt.plot(xvals[1:],testtest[1:],color = 'yellow',label = 'total',linewidth = 3)
	plt.plot(xvals[1:],diffmass[1:],color = 'black',label = 'Actual Diff',linewidth = 3)
#	plt.plot(xvals[1:],diffdiff[1:],color = 'darkred',label = 'diffdiff',linewidth=3)
    
	plt.title("Condensate Mass Budget",fontsize = 23)
	plt.xlabel("Minutes",fontsize = 19 )
	plt.ylabel('Mass Change in '+str(dt)+'s (10$^6$ kg)',fontsize = 19 )

	plt.legend(loc = 'best')
	plt.savefig("/nobackup/rstorer/plots/test2s/budget"+xdir+"2s.png")
	plt.clf()



	plt.plot(xvals,totalmass,linewidth=3)
	plt.savefig('../plots/test2s/totalcond'+xdir+'2s.png')
	plt.clf()
    

    
    
maindir = '/nobackup/rstorer/convperts/revu2s/'
modeldirs = os.walk(maindir).next()[1]
dx = 250
dy = 250
dt = 2
for xdir in modeldirs:
	print xdir
	budgetplot(maindir, xdir, dx, dy, dt)

