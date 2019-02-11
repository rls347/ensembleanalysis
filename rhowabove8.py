import numpy as np
import copy
import matplotlib
matplotlib.use("Agg")
import glob
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar,getrho,getdz
from rachelutils.dumbnaming import pert75

height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')
h8km = np.argmin(np.abs(height-8000))
height=height[h8km:]
dz = getdz('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5')[h8km:]

modeldirs = pert75()


modeldirs = ['feb23-control','aug11-control','aug17-control']

updraftfrac = {}

plt.set_cmap('summer')

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nt = len(files)
    uptimes = np.zeros(nt)
    downtimes = np.zeros(nt)
    for t in range(nt):
        w = (getvar(files[t],'w')[h8km:,:,:])
        rho = getrho(files[t])[h8km::,10,10]
        cond = (getvar(files[t],'total_cond')[h8km:,:,:])
        flux = w*rho[:,None,None]*dz[:,None,None]
        
        inboth = np.where(np.logical_and(cond>0.1,w>2))
        inbothdown = np.where(np.logical_and(cond>0.1,w<-2))

        if len(inboth[0]) >1:

            sumdz = np.sum(dz[:np.max(np.asarray(inboth[0]))])

            fluxup = copy.deepcopy(flux)
            fluxdown = copy.deepcopy(flux)

            fluxup[w<2]=0.
            fluxdown[w>-2]=0.
            fluxup[cond<0.1]=0.
            fluxdown[cond<0.1]=0.

            fup = np.sum(fluxup,0)/sumdz
            fdn = np.sum(fluxdown,0)/sumdz

            uptimes[t] = np.sum(fup) * 250*250.
            downtimes[t] =  np.sum(fdn) * 250*250.


            xvar = np.arange(400)*.25
            plt.contourf(xvar,xvar,fup)
            plt.colorbar(label = 'kg/m$^2$s')
            plt.title('Upward Flux >8km')
            plt.savefig('upwardflux'+str(t)+'.png')
            plt.clf()

            plt.contourf(xvar,xvar,fdn)
            plt.colorbar(label = 'kg/m$^2$s')
            plt.title('Downward Flux >8km')
            plt.savefig('downardflux'+str(t)+'.png')
            plt.clf()
    
    uf = np.sum(uptimes)/np.sum(downtimes)
    updraftfrac[xdir]=uf

    xs = np.arange(nt)*5
    plt.plot(xs,uptimes,color='red',linewidth=3)
    plt.plot(xs,downtimes,color='blue',linewidth=3)
    plt.xlabel('Minutes')
    plt.ylabel('kg/s')
    plt.title(xdir+': updraft/downdraft (2m/s) = '+str(uf)) 
    plt.savefig('fluxtimeratesabove8-'+xdir+'-2ms.png')
    plt.clf()

    print xdir, np.sum(uptimes)*300, np.sum(downtimes)*300, np.sum(uptimes)/np.sum(downtimes)


#np.savez('updraftfraction2ms.npz',**updraftfrac)        

        




