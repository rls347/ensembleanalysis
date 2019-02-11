import numpy as np
import h5py as hdf
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 

#Some constants
cp = 1004.
rd = 287.
kappa = rd/cp
ps = 1000.

filesrams = sorted(glob.glob("/nobackup/rstorer/convperts/mature/feb23-control/*h5"))

onefile = '/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5'
fil = hdf.File(onefile, 'r')
height = fil['z_coords'].value
w=np.squeeze(fil['w'].value[0,39,:,:])
val = np.unravel_index(w.argmax(), w.shape)
fil.close()

dz = np.zeros_like(height)
dz[0:-1]=height[1:]-height[:-1]
dz[-1]=dz[-2]

dx = 250.
dy = 250.
dt = 30.

nt=len(filesrams)

totalmass = np.zeros(nt)
totalmicro = np.zeros(nt)
detrain = np.zeros(nt)
advect = np.zeros(nt)
vertical = np.zeros(nt)
pcp = np.zeros(nt)
detrainslice = np.zeros((nt,82))


#46 161 238
#midx = 150
#midy = 250

midx = val[0]
midy = val[1]

print midx, midy

axx = midx-50
bxx = midx+50
ayy = midy-50
byy = midy+50


#axx = 5 
#bxx = 395 
#ayy = 5 
#byy = 395 
azz = 39#46
bzz = 80



for t in range(nt):
    ramsfile = hdf.File(filesrams[t],"r")
    q = np.squeeze(ramsfile['total_cond'].value )/1000.
    microdiff = np.squeeze(ramsfile['nuccldrt'].value + ramsfile['nucicert'].value \
                + ramsfile['vapliqt'].value + ramsfile['vapicet'].value)  / 1000.
    if t ==0:
        microdiff = microdiff*0.0
    precip = np.squeeze(ramsfile['precip3d'].value) * -1.
    w = np.squeeze(ramsfile['w'].value)
    u = np.squeeze(ramsfile['u'].value)
    v = np.squeeze(ramsfile['v'].value)
    press = np.squeeze(ramsfile['press'].value) * 100. 
    tempk = np.squeeze(ramsfile['tempk'].value) 
    rho = press / (rd*tempk)   
    ramsfile.close()  
    
    meanu = np.zeros((82,1,1),dtype = float)
    uprime = np.zeros((82,400,400),dtype = float)
    meanv = np.zeros_like(meanu)
    vprime = np.zeros_like(uprime)
    

    for k in xrange(82):
        meanu[k,:,:] = np.mean(u[k,:,:])   
        uprime[k,:,:] = u[k,:,:] - meanu[k,:,:]
        meanv[k,:,:] = np.mean(v[k,:,:])   
        vprime[k,:,:] = v[k,:,:] - meanv[k,:,:]
    
    
    rhouqp = rho * uprime * q
    rhovqp = rho * vprime * q
    advu = rho * meanu * q
    advv = rho * meanv * q
    advw = rho * w * q

    if t ==10:
        plt.contourf(advw[azz,:,:])
        plt.colorbar()
        cur=plt.gca()
        cur.add_patch(Rectangle((ayy,axx),50,50))
        plt.savefig('massflux-feb23-control-smaller-mature.png')
        plt.clf()
        plt.contourf(w[azz,:,:])
        plt.colorbar()
        cur=plt.gca()
        cur.add_patch(Rectangle((ayy,axx),50,50))
        plt.savefig('w500-feb23-control-smaller-mature.png')
        plt.clf()
    

    print t, np.sum(q[46:,:,:])
    
    detrainx = np.zeros(82)
    detrainy = np.zeros(82)
    for k in range(82):
        left = np.sum(rhouqp[k,axx:bxx,ayy]) * dz[k] * dy * dt
        right = np.sum(rhouqp[k,axx:bxx,byy]) * dz[k] * dy * dt
        detrainx[k] = left-right
        
        up = np.sum(rhovqp[k,bxx,ayy:byy]) * dz[k] * dy * dt
        down = np.sum(rhovqp[k,axx, ayy:byy]) * dz[k] * dy * dt
        detrainy[k] = down - up
        
       
    advectx = np.zeros(82)
    advecty = np.zeros(82)
    for k in range(82):
        leftarray = np.sum(advu[k,axx:bxx,ayy]) * dz[k] * dy * dt
        rightarray = np.sum(advu[k,axx:bxx,byy]) * dz[k] * dy * dt
        advectx[k] = leftarray - rightarray
        uparray = np.sum(advv[k,bxx,ayy:byy]) * dz[k] * dx * dt
        downarray = np.sum(advv[k,axx, ayy:byy]) * dz[k] * dx * dt
        advecty[k] = downarray - uparray      
    
    dzslice = np.zeros((82,400,400))
    for k in range(82):
        dzslice[k,:,:] = dz[k]

	detrainslice[t,:]=detrainx+detrainy
    
    vertical[t] = dx * dy * dt * (np.sum(advw[azz,axx:bxx,ayy:byy])-np.sum(advw[bzz,axx:bxx,ayy:byy]))
    
    detrain[t] = np.sum(detrainx[azz:bzz]+detrainy[azz:bzz])
    advect[t] = np.sum(advectx[azz:bzz]+advecty[azz:bzz])
    
    pcp[t] = dx * dy * dt * (np.sum(precip[azz,axx:bxx,ayy:byy])-np.sum(precip[bzz,axx:bxx,ayy:byy]))    
   
#    totalmass[t]  = np.sum(q[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy] *dzslice[azz:bzz,axx:bxx,ayy:byy]) * dx * dy
    tmpvar = q*rho*dzslice
    totalmass[t] = np.sum(tmpvar[azz:bzz,axx:bxx,ayy:byy]) * dx * dy
     
    totalmicro[t] = np.sum(microdiff[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
        *dzslice[azz:bzz,axx:bxx,ayy:byy]) * dx * dy
        
   

diffmass = np.diff(totalmass)


tots = detrain + advect + vertical + totalmicro + pcp


diffmass = diffmass/1e6
detrain = detrain/1e6
advect = advect/1e6
vertical=vertical/1e6
totalmicro = totalmicro/1e6
pcp = pcp / 1e6
tots = tots/1e6
totvert = vertical+pcp

xs = np.arange(nt)*.5
detrainslice = np.rollaxis(detrainslice,1)
plt.contourf(xs,height,detrainslice)
plt.colorbar()
plt.savefig('detrainprof-feb23-control-smaller-mature.png')
plt.clf()

#plt.plot(totvert,color='green',label = "vertical",linewidth=3)
plt.plot(detrain, color = 'red', label = "detrainment", linewidth=3)
plt.plot(advect,  color = 'blue', label = "advection", linewidth=3)
plt.plot(vertical, color= 'green', label = "updraft", linewidth=3)
plt.plot(totalmicro,  color='purple', label = "microphys", linewidth=3)
plt.plot(pcp,  color = 'orange', label = "precip", linewidth=3)
plt.plot(tots, color = 'black', label = "total",linewidth=3)
plt.plot(diffmass, color = 'yellow', label = 'mass diff',linewidth=3)
plt.legend()
plt.savefig('wholeUTbudget-feb23-control-smaller-mature.png')
plt.clf()

plt.plot(totalmass)
plt.savefig('wholeUT-totalmass-feb23-control-smaller-mature.png')

