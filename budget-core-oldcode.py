import numpy as np
import h5py as hdf
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from netCDF4 import Dataset

#Some constants
cp = 1004.
rd = 287.
kappa = rd/cp
ps = 1000.



filesrams = glob.glob("/nobackup/rstorer/convperts/mature-orig/feb23-control/out*h5")

onefile = '/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5'
fil = hdf.File(onefile, 'r')
height = fil['z_coords'].value
fil.close()
dz = np.zeros_like(height)
dz[0:-1]=height[1:]-height[:-1]
dz[-1]=dz[-2]

#height = np.loadtxt('/Users/rachelstorer/work/rams/saleebytropical/z.txt', dtype=float)
#heightzm = np.loadtxt('/Users/rachelstorer/work/rams/saleebytropical/zm.txt', dtype=float)
#dz = np.zeros_like(height)
#dz[1:69] = heightzm[1:69]-heightzm[:68]
#dz[-1]=dz[-2]

dx = 250.
dy = 250.
dt = 30.


totalmass = np.zeros(60)
totalmicro = np.zeros(60)
detrain = np.zeros(60)
advect = np.zeros(60)
vertical = np.zeros(60)
pcp = np.zeros(60)


#46 161 238
midx = 150
midy = 250

axx = midx-100
bxx = midx+100
ayy = midy-100
byy = midy+100
azz = 46
bzz = 80


maxwtimes = np.zeros(60)

for t in xrange(60):
    ramsfile = hdf.File(filesrams[t],"r")
    q = ramsfile['RCP'].value + ramsfile['RRP'].value + ramsfile['RPP'].value \
                + ramsfile['RSP'].value + ramsfile['RAP'].value + ramsfile['RGP'].value \
                + ramsfile['RHP'].value + ramsfile['RDP'].value
    microdiff = ramsfile['NUCCLDRT'].value + ramsfile['NUCICERT'].value \
                + ramsfile['VAPLIQT'].value + ramsfile['VAPICET'].value
    precip = ramsfile['PCPVR'].value + ramsfile['PCPVP'].value + ramsfile['PCPVS'].value + ramsfile['PCPVA'].value \
                + ramsfile['PCPVG'].value + ramsfile['PCPVH'].value + ramsfile['PCPVD'].value
    w = ramsfile['WC'].value
    u = ramsfile['UC'].value
    v = ramsfile['VC'].value
    press = ( ( ramsfile['PI'].value/cp )**(1/kappa) ) * ps * 100   #pascals
    tempk = ( ramsfile['PI'].value/cp ) * ramsfile['THETA'].value
    rho = press / (rd*tempk)   
    ramsfile.close()  
    
    meanu = np.zeros((82,1,1),dtype = float)
    uprime = np.zeros((82,400,400),dtype = float)
    meanv = np.zeros_like(meanu)
    vprime = np.zeros_like(uprime)
    
    maxwtimes[t]=np.mean(w[azz,axx:bxx,ayy:byy])

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
    
    precip = precip * -1

    
        
    #cloudtop = np.max(np.where(q[t,:,axx:bxx,ayy:byy] > (0.01/1000)))
    #cloud top ranges from azz to 51, so using that as range...top 2.5 km  
#    if t ==0:
#        maxw = np.max(w,axis=0)
#        new = np.where(maxw > 1) 
#        axx = min(new[0])
#        bxx = max(new[0])
#        ayy = min(new[1])
#        byy = max(new[1])
    
    print t
    
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
    
    
    vertical[t] = dx * dy * dt * (np.sum(advw[azz,axx:bxx,ayy:byy])-np.sum(advw[bzz,axx:bxx,ayy:byy]))
    
    detrain[t] = np.sum(detrainx[azz:bzz]+detrainy[azz:bzz])
    advect[t] = np.sum(advectx[azz:bzz]+advecty[azz:bzz])
    
    pcp[t] = dx * dy * dt * (np.sum(precip[azz,axx:bxx,ayy:byy])-np.sum(precip[bzz,axx:bxx,ayy:byy]))    
   
#    totalmass[t]  = np.sum(q[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy] *dzslice[azz:bzz,axx:bxx,ayy:byy]) * dx * dy
    tmpvar = q*rho*dzslice
    totalmass[t] = np.sum(tmpvar[azz:bzz,axx:bxx,ayy:byy])
     
    totalmicro[t] = np.sum(microdiff[azz:bzz,axx:bxx,ayy:byy]*rho[azz:bzz,axx:bxx,ayy:byy]\
        *dzslice[azz:bzz,axx:bxx,ayy:byy]) * dx * dy
        
   

diffmass = np.diff(totalmass)

for t in range(1,30):
    print t, diffmass[t]/diffmass[t], detrain[t]/diffmass[t], vertical[t]/diffmass[t], advect[t]/diffmass[t], pcp[t]/diffmass[t], totalmicro[t]/diffmass[t]

tots = detrain + advect + vertical + totalmicro + pcp


diffmass = diffmass/1e6
detrain = detrain/1e6
advect = advect/1e6
vertical=vertical/1e6
totalmicro = totalmicro/1e6
pcp = pcp / 1e6
tots = tots/1e6



plt.plot(detrain, color = 'red', label = "detrainment", linewidth=3)
plt.plot(advect,  color = 'blue', label = "advection", linewidth=3)
plt.plot(vertical, color= 'green', label = "updraft", linewidth=3)
plt.plot(totalmicro,  color='purple', label = "microphys", linewidth=3)
plt.plot(pcp,  color = 'orange', label = "precip", linewidth=3)
plt.plot(tots, color = 'black', label = "total",linewidth=3)
plt.plot(diffmass, color = 'yellow', label = 'actual',linewidth=3)
plt.legend()
plt.savefig('testcoreplot-oldcode.png')
plt.clf()

plt.plot(totalmass)
plt.savefig('testcoreplot-totalmass.png')

