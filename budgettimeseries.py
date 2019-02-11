import numpy as np
import h5py as hdf
import glob
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pdb

def budgetplot(maindir, xdir, dx, dy, dt):
	files = sorted(glob.glob(maindir+xdir+'/*.h5'))
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
		qc = (np.squeeze(f['cloud'].value) ) / 1000.
		qd = (np.squeeze(f['drizzle'].value) ) / 1000.
		qr = (np.squeeze(f['rain'].value) ) / 1000.
		qp = (np.squeeze(f['pristine'].value) ) / 1000.
		qa = (np.squeeze(f['aggregates'].value) ) / 1000.
		qh = (np.squeeze(f['hail'].value) ) / 1000.
		qs = (np.squeeze(f['snow'].value) ) / 1000.
		qg = (np.squeeze(f['graupel'].value) ) / 1000.
		microdiff = (np.squeeze(f['nuccldrt'].value + f['nucicert'].value + f['vapliqt'].value + f['vapicet'].value)) / 1000. 
		nuc_liq= (np.squeeze(f['nuccldrt'].value)) /1000.
		nuc_ice = (np.squeeze(f['nucicert'].value)) /1000.
		vap_liq = (np.squeeze(f['vapliqt'].value)) / 1000.
		vap_ice = (np.squeeze(f['vapicet'].value)) / 1000.
		precip = np.squeeze(f['precip3d'].value)
		height = np.squeeze(f['z_coords'].value)
		f.close()
		dz = np.zeros_like(height)
		dz[:-1] = np.diff(height)
		dz[-1] = dz[-2]
		qdz = q*dz[:,None,None]
		qcdz = qc*dz[:,None,None]
		qddz = qd*dz[:,None,None]
		qrdz = qr*dz[:,None,None]
		qpdz = qp*dz[:,None,None]
		qsdz = qs*dz[:,None,None]
		qadz = qa*dz[:,None,None]
		qgdz = qg*dz[:,None,None]
		qhdz = qh*dz[:,None,None]
		nz = q.shape[0]
		nx = q.shape[1]
		ny = q.shape[2]
		azz = np.argmin(np.absolute(height-8000))
		bzz = nz-1
		if t ==0:
			maxwval = np.max(w)
			places = np.where(w == maxwval)
			midx = places[1][0]
			midy = places[2][0]
			print midx, midy
		
		axx = midx - (2500/dx)
		bxx = midx + (2500/dx)
		ayy = midy - (2500/dy)
		byy = midy + (2500/dy)

        #bzz = nz-1
        #axx = nx/2 - (2500/dx)
        #bxx = nx/2 + (2500/dx)
        #ayy = ny/2 - (2500/dy)
        #byy = ny/2 + (2500/dy)

        # azz = 5
        # axx = nx/2 - (25000/dx)
        # bxx = nx/2 + (25000/dx)
        # ayy = ny/2 - (25000/dy)
        # byy = ny/2 + (25000/dy)
        #
        
        
		meanu = np.mean((np.mean(u,1)),1)
		meanv = np.mean((np.mean(v,1)),1)
		vprime = v - meanv[:,None,None]
		uprime = u - meanu[:,None,None]
		
		rhouqp = rho * uprime * q
		rhovqp = rho * vprime * q

		qmid = np.zeros_like(q)
		wmid = np.zeros_like(w)
		for hg in range(1,nz-1):
			tmp1 = rho[hg,:,:] * q[hg,:,:]
			tmp2 = rho[hg+1,:,:] * q[hg+1,:,:]
			qmid[hg,:,:] = np.mean( np.array([ tmp1, tmp2 ]), axis=0 )
			tmp3 = w[hg,:,:]
			tmp4 = w[hg-1,:,:]
			wmid[hg,:,:] = np.mean( np.array([ tmp3, tmp4 ]), axis=0 )
		
		advu = rho * meanu[:,None,None] * q
		advv = rho * meanv[:,None,None] * q
		advw = q* wmid 
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
		nucice[t] = np.sum(nuc_ice[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
		nucliq[t] = np.sum(nuc_liq[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
		vapliq[t] = np.sum(vap_liq[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
		vapice[t] = np.sum(vap_ice[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
            *dz[azz:bzz,None,None]) * dx * dy
        
		condabove8[t] = np.sum(qdz[azz:,axx:bxx,ayy:byy])*dx*dy                        
		cloud[t] = np.sum(qcdz[azz:,axx:bxx,ayy:byy])*dx*dy
		drizzle[t] = np.sum(qddz[azz:,axx:bxx,ayy:byy])*dx*dy
		rain[t] = np.sum(qrdz[azz:,axx:bxx,ayy:byy])*dx*dy
		pristine[t] = np.sum(qpdz[azz:,axx:bxx,ayy:byy])*dx*dy
		snow[t] = np.sum(qsdz[azz:,axx:bxx,ayy:byy])*dx*dy
		aggregates[t] = np.sum(qadz[azz:,axx:bxx,ayy:byy])*dx*dy
		graupel[t] = np.sum(qgdz[azz:,axx:bxx,ayy:byy])*dx*dy
		hail[t] = np.sum(qhdz[azz:,axx:bxx,ayy:byy])*dx*dy



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
	plt.plot(xvals[1:],diffdiff[1:],color = 'darkred',label = 'diffdiff',linewidth=3)
    
	plt.title("Condensate Mass Budget",fontsize = 23)
	plt.xlabel("Minutes",fontsize = 19 )
	plt.ylabel('Mass Change in '+str(dt)+'s (10$^6$ kg)',fontsize = 19 )

	plt.legend(loc = 'best')
	plt.savefig("/nobackup/rstorer/plots/testrevubudget-maxwbox-budget30s"+xdir+".png")
	plt.clf()

	plt.plot(xvals[1:],nucliq[1:], color = 'red', label = 'nuccloud', linewidth = 3)
	plt.plot(xvals[1:],nucice[1:], color = 'blue', label = 'nucice', linewidth = 3)
	plt.plot(xvals[1:],vapliq[1:], color = 'purple', label = 'vapliq', linewidth = 3)
	plt.plot(xvals[1:],vapice[1:],color = 'yellow',label = 'vapice',linewidth = 3)
	plt.legend(loc = 'best')
	plt.savefig('/nobackup/rstorer/plots/testrevubudget-maxwbox-budget30s-micro-revu-'+xdir+'.png')
	plt.clf()

#
#	plt.plot(condabove8)
#	plt.savefig('../plots/maxwbox'+xdir+'revu.png')
#	plt.clf()
#
#	plt.plot(xvals[1:],cloud[1:], color = 'orange', label = 'cloud', linewidth = 3)
#	plt.plot(xvals[1:],drizzle[1:], color = 'darkgreen', label = 'drizzle', linewidth = 3)
#	plt.plot(xvals[1:],rain[1:], color = 'lightgreen', label = 'rain', linewidth = 3)
#	plt.plot(xvals[1:],pristine[1:], color = 'red', label = 'pristine', linewidth = 3)
#	plt.plot(xvals[1:],snow[1:], color = 'blue', label = 'snow', linewidth = 3)
#	plt.plot(xvals[1:],aggregates[1:], color = 'purple', label = 'aggregates', linewidth = 3)
#	plt.plot(xvals[1:],graupel[1:],color = 'yellow',label = 'graupel',linewidth = 3)
#	plt.plot(xvals[1:],hail[1:],color = 'black',label = 'hail',linewidth = 3)
#	plt.plot(xvals[1:],condabove8[1:],color = 'darkred',label = 'totalcond',linewidth=3)
#	plt.legend(loc = 'best')
#	plt.savefig('/nobackup/rstorer/plots/maxwbox-hydrometeors-revu-'+xdir+'.png')
#	plt.clf()
#
#	liq = cloud+rain+drizzle
#	ice = pristine+snow+aggregates+graupel+hail
#	plt.plot(xvals[1:],liq[1:],color = 'blue',label = 'liquid', linewidth = 3)
#	plt.plot(xvals[1:],ice[1:],color = 'red',label = 'ice',linewidth = 3)
#	plt.legend(loc='best')
#	plt.savefig('../plots/maxwbox-hydrometeor-liqice-revu-'+xdir+'.png')
#	plt.clf()

    

    
    
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = os.walk(maindir).next()[1]
modeldirs = ['feb23-control','aug11-control','aug17-control']
dx = 250
dy = 250
dt = 300
for xdir in modeldirs:
	print xdir
	budgetplot(maindir, xdir, dx, dy, dt)

