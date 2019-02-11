import matplotlib
matplotlib.use("Agg")
import numpy as np
import math
import h5py as hdf
import matplotlib.pyplot as plt
import os
import glob

def findmid(dirname):
	files = sorted(glob.glob(dirname+'/*h5'))
	nt = len(files)
	w = np.zeros((nt-1,4))
	wh = np.zeros(nt-1)
	maxw = np.zeros(nt-1)
	for tim in range(nt-1):
		fil = hdf.File(files[tim+1],'r')
		maxw[tim] = np.max(fil['w'].value)
		w[tim,:]=np.where(fil['w'].value == maxw[tim]) 
		height = fil['z_coords'].value
		wh[tim] = height[w[tim,1]]
	

	return (np.argmin(np.absolute(height-10000)),int(math.floor(np.mean(w[:,2]))),int(math.floor(np.mean(w[:,3]))))

def budget(dirname,kk, ii, jj, run, extrastring):
    files = sorted(glob.glob(dirname+'/*h5'))
    nt = len(files)
    cmf = np.zeros(nt)
    pcp3d = np.zeros(nt)
    mass = np.zeros(nt)
    mic = np.zeros(nt)
    adv = np.zeros(nt)
    det = np.zeros(nt)
    diffmass = np.zeros(nt)

    for tim in range(nt):
        fil = hdf.File(files[tim],'r')
        w = np.squeeze(fil['w'].value)
        u = np.squeeze(fil['u'].value)
        v = np.squeeze(fil['v'].value)
        cond = np.squeeze(fil['total_cond'].value)/1000. #g/kg to kg/kg
        rho = (100*np.squeeze(fil['press'].value)) /(287 * np.squeeze(fil['tempk'].value))  #rho = P*100/RT
        precip = np.squeeze(fil['precip3d'].value)
        micro = (np.squeeze(fil['nuccldrt'].value) + np.squeeze(fil['nucicert'].value) + np.squeeze(fil['vapicet'].value) + np.squeeze(fil['vapliqt'].value))/1000. #kg/kg
        height = fil['z_coords'].value
		
        dz = np.zeros_like(height)
        dz[0:-1] = height[1:]-height[0:-1]
        dz[-1] = dz[-2]
    
        meanu = np.mean(np.mean(u,2),1)
        meanv = np.mean(np.mean(v,2),1)
        vprim = v-meanv[:,None,None]
        uprim = u-meanu[:,None,None]


        massflux = w*cond*rho   # m/s * kg/kg * kg/m3 = kg/m2s
        micro = (micro * rho * dz[:,None,None]) /30. # kg/kg * kg/m3 m/30s = kg/m2s 
        cond3 = cond * rho * dz[:,None,None]  # kg/kg * kg/m3 * m = kg/m2
        vadv = cond * rho * meanv[:,None,None] * dz[:,None,None] #kg/kg * kg/m3 * m/s * m = kg/ms
        uadv = cond * rho * meanu[:,None,None] * dz[:,None,None]
        vdet = cond * rho * vprim * dz[:,None,None]
        udet = cond * rho * uprim * dz[:,None,None]

 
		# cmf and precip3d occur only at bottom edge
        cmf[tim] = np.sum(massflux[kk,ii-20:ii+20,jj-20:jj+20]) * (20*250)*(20*250) # 5km box each way; units of cmf kg/s #changed to 10km
        pcp3d[tim] = np.sum(precip[kk,ii-20:ii+20,jj-20:jj+20]) * (20*250)*(20*250) * -1.0 #should be a sink. 

		# actual mass change and change for micro should be 3d
        mass[tim] = np.sum(cond3[kk:-1,ii-20:ii+20,jj-20:jj+20]) * (20*250)*(20*250)  #actual mass is kg - need to diff and /30 for kg/s
        mic[tim] = np.sum(micro[kk:-1,ii-20:ii+20,jj-20:jj+20]) * (20*250)*(20*250)  #kg/s

		#horizontal velocity components are 2d integrals (zx or zy)
        det[tim] = np.sum(vdet[kk:-1,ii-20,jj-20:jj+20] + udet[kk:-1,ii-20:ii+20,jj-20] 
						- vdet[kk:-1,ii+20,jj-20:jj+20] - udet[kk:-1,ii-20:ii+20,jj+20]) * (20*250) #kg/ms * one x/y dir = kg/s
        adv[tim] = np.sum(vadv[kk:-1,ii-20,jj-20:jj+20] + uadv[kk:-1,ii-20:ii+20,jj-20] 
						- vadv[kk:-1,ii+20,jj-20:jj+20] - uadv[kk:-1,ii-20:ii+20,jj+20]) * (20*250) #kg/ms * one x/y dir = kg/s

		#if tim > 1:
			#print cmf[tim]/10000000., pcp3d[tim]/10000000.,(mass[tim]-mass[tim-1])/10000000., det[tim]/10000000., adv[tim]/10000000.

    diffmass[1:] = (mass[1:]-mass[0:-1]) /30. #kg/s
    diffmass[0]=diffmass[1]
    sumsum = cmf + pcp3d + mic + det + adv
    vert = cmf+pcp3d

	#plt.plot(cmf[1:], color = 'red', label = 'Updraft', linewidth = 3)
	#plt.plot(pcp3d[1:], color = 'blue', label = 'Precip', linewidth = 3)
    plt.plot(vert[1:],color = 'red', label = 'Vertical Flux', linewidth =3)
    plt.plot(det[1:], color = 'orange', label = 'Detrainment', linewidth = 3)
    plt.plot(adv[1:], color = 'purple', label = 'Advection', linewidth = 3)
    plt.plot(mic[1:], color = 'green', label = 'Microphys', linewidth = 3)
    plt.plot(sumsum[1:], color = 'yellow', label = 'Sum', linewidth = 3)
    plt.plot(diffmass[1:], color = 'black', label = 'Mass Diff', linewidth = 3)
    plt.legend()
    plt.savefig('../plots/budgetslices/testbudgetnew'+run+extrastring+'.png')
    plt.clf()


dirname = '/nobackup/rstorer/convperts/mature/aug11-control'
#kk, ii,jj = findmid(dirname)
#budget(dirname, kk, 190, 275, 'aug11-control','.mature.190y.275x.conv')
#budget(dirname, kk, 200, 240, 'aug11-control','.mature.125y.275x.strat')
#print kk, ii, jj, dirname
dirname = '/nobackup/rstorer/convperts/mature/aug17-control'
#kk, ii,jj = findmid(dirname)
#budget(dirname, kk, 150, 225, 'aug11-control','.mature.150y.225x.conv')
#budget(dirname, kk, 200, 225, 'aug11-control','.mature.200y.225x.strat')
#print kk, ii, jj, dirname
dirname = '/nobackup/rstorer/convperts/mature/feb23-control'
kk, ii,jj = findmid(dirname)
budget(dirname, kk, ii,jj, 'feb23-control','.mature.maxw.conv')
#budget(dirname, kk, 125, 275, 'feb23-control','.mature.125y.275x.conv')
#budget(dirname, kk, 150, 275, 'feb23-control','.mature.150y.275x.strat')
#budget(dirname, kk, 125, 250, 'feb23-control','.mature.125y.250x.strat')



print kk, ii, jj, dirname

