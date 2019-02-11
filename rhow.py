import numpy as np
import matplotlib
matplotlib.use("Agg")
import glob
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar,getrho
from rachelutils.dumbnaming import pert75

height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')
h8km = np.argmin(np.abs(height-8000))
modeldirs = pert75()
actupcond = {}
actupboth = {}
actupup = {}
estup = {}
actdownboth = {}

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/'+xdir+'/*h5'))
    nt = len(files)
    estup[xdir] = np.zeros(nt)
    actupup[xdir] = np.zeros(nt)
    actupcond[xdir] = np.zeros(nt)
    actupboth[xdir] = np.zeros(nt)
    actdownboth[xdir] = np.zeros(nt)

    for t in range(nt):
        w = (getvar(files[t],'w')[h8km,:,:]).flatten()
        rho = np.mean(getrho(files[t])[h8km,:,:])
        cond = (getvar(files[t],'total_cond')[h8km,:,:]).flatten()
        
        incloud = np.where(cond>0.1)
        inup = np.where(w>1)
        inboth = np.where(np.logical_and(cond>0.1,w>1))
        inbothdown = np.where(np.logical_and(cond>0.1,w<-1))

        if len(incloud[0]) >1:
            sigma = 1.0*len(inup[0])/len(incloud[0])
            estup[xdir][t] = rho*sigma*np.mean(w[inboth])
            actupboth[xdir][t] = np.mean(rho*w[inboth])
            actupcond[xdir][t] = np.mean(rho*w[incloud])
            actupup[xdir][t] = np.mean(rho*w[inup])

            actdownboth[xdir][t] = np.mean(rho*w[inbothdown])

    xs = np.arange(nt)*.5
    plt.plot(xs,estup[xdir],color = 'gray',linewidth=3)
    plt.plot(xs,actupboth[xdir],color='black',linewidth=3)
    plt.plot(xs,actupup[xdir],color='red',linewidth=3)
    plt.plot(xs,actupcond[xdir],color='blue',linewidth=3)
    plt.plot(xs,actdownboth[xdir],color='green',linewidth=3)
    plt.axhline(color='gray',linestyle='dashed') 
    plt.title('Growing, 8km: '+xdir)
    plt.xlabel('Minutes')
    plt.ylabel('Mass Flux (kg/m$^2$s)')
    plt.savefig('mature'+xdir+'massfluxestimate.png')
    plt.clf()

np.savez('mature-8kmflux-estimate1.npz',**estup)
np.savez('mature-8kmflux-actualupcond1.npz',**actupcond)
np.savez('mature-8kmflux-actualupup1.npz',**actupup)
np.savez('mature-8kmflux-actualupboth1.npz',**actupboth)
np.savez('mature-8kmflux-actualdownboth1.npz',**actdownboth)
        

        

        




