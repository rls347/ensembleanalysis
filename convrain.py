import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def precipmovie(maindir, modeldirs, dirout):
    filename = '/nobackup/rstorer/filesnpz/growingcloudtops.npz'
    varall = np.load(filename)
    for xdir in modeldirs:
        cloudtop = varall[xdir]
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['pcprate'].value))
        pcp = np.asarray(pcp)
        
        xs = np.arange(pcp.shape[1])*(100./pcp.shape[1])
        ys = xs
        high = np.where(cloudtop > 6000)
        low = np.where(cloudtop < 6000)

        fig = plt.figure()
        z2 = pcp[0,:,:]
        lowpcp = np.where(z2<25.4)
        z2[lowpcp] = 0
        cont2 = plt.contourf(xs,ys,z2,levels=np.arange(25.,np.max(pcp)))
        c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")

        def animate(i):
            z2 = pcp[i,:,:]
            lowpcp = np.where(z2<25.4)
            z2[lowpcp] = 0
            plt.clf()
            cont2 = plt.contourf(xs,ys,z2,levels=np.arange(25.,np.max(pcp)))
            c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")
            title='Time ' + str(i)
            plt.title(title)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'gt1inchgrowingprecip.mp4')
        plt.clf()


        pcp[low] = pcp[low]*-1
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        cont2 = plt.contourf(xs,ys,z2,levels=np.arange(0.1,np.max(pcp)))
        c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            plt.clf()
            cont2 = plt.contourf(xs,ys,z2,levels=np.arange(0.1,np.max(pcp)))
            c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")
            title='Time ' + str(i)
            plt.title(title)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'highcloudgrowingprecip.mp4')
        plt.clf()

        fig = plt.figure()
        z2 = pcp[0,:,:]
        cont2 = plt.contourf(xs,ys,z2,levels=np.arange(np.min(pcp),-0.1))
        c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            plt.clf()
            cont2 = plt.contourf(xs,ys,z2,levels=np.arange(np.min(pcp),-0.1))
            c2 = plt.colorbar(cont2,label = "Precip Rate (mm/hr)")
            title='Time ' + str(i)
            plt.title(title)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'lowcloudgrowingprecip.mp4')
    

########################################

maindir = '/nobackup/rstorer/convperts/growing/'
modeldirs = os.walk(maindir).next()[1]
modeldirs = ['aug11-control','aug17-control','feb23-control']
dirout = '/nobackup/rstorer/plots/'

precipmovie(maindir, modeldirs, dirout)

