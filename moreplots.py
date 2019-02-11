import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def precipmovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['pcprate'].value))
        pcp = np.asarray(pcp)
        
        xs = np.arange(pcp.shape[1])#*(100./pcp.shape[1])
        ys = xs
            
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
        anim.save(dirout+xdir+'precipmature.mp4')
    
def vertcondmovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['vertint_cond'].value))
        pcp = np.asarray(pcp)
        
        xs = np.arange(pcp.shape[1])*(100./pcp.shape[1])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        cont2 = plt.contourf(xs,ys,z2,levels=np.arange(0,np.max(pcp)))
        c2 = plt.colorbar(cont2,label = "Vertical Integrated Condensate (mm)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,ys,z2,levels=np.arange(0,np.max(pcp)))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'vertcond.mp4')

def logvertcondmovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['vertint_cond'].value))
        pcp = np.asarray(pcp)
        
        xs = np.arange(pcp.shape[1])*(100./pcp.shape[1])
        ys = xs
        fig = plt.figure()
        z2 = pcp[0,:,:]
        cont2 = plt.contourf(xs,ys,z2,levels=np.logspace(-2, np.log10(np.max(pcp)),20))
        c2 = plt.colorbar(cont2,label = "Vertical Integrated Condensate (mm)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,ys,z2,levels=np.logspace(-2, np.log10(np.max(pcp)),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'logvertcond.mp4')

def logcondslicemovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['total_cond'].value)[:,148,:])
            
        pcp = np.asarray(pcp)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.logspace(-2, np.log10(np.max(pcp)),20))
        c2 = plt.colorbar(cont2,label = "Total Condensate Slice (y=37km)(g/kg)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.logspace(-2, np.log10(np.max(pcp)),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'logcondslice.mp4')
        
def condslicemovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['total_cond'].value)[:,148,:])
            
        pcp = np.asarray(pcp)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "Total Condensate Slice (y=37km)(g/kg)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'condslice.mp4')
        
def wslicemovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['w'].value)[:,148,:])
            
        pcp = np.asarray(pcp)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "Vertical Velocity Slice (y=37km)(m/s)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'wslice.mp4')        
        
def condandwslicemovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        pcpw = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['total_cond'].value)[:,148,:])
            pcpw.append(np.squeeze(fil['w'].value)[:,148,:])
        pcp = np.asarray(pcp)
        pcpw = np.asarray(pcpw)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        w = pcpw[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "Total Condensate Slice (y=37km)(g/kg)")
        #plt.contour(xs,height,w, levels = [5,10,20])
        plt.title('Filled: Total Cond, Contours: w = 5,10,20 m/s')
        
        def animate(i): 
            z2 = pcp[i,:,:]
            w = pcpw[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0, np.max(pcp),20))
            plt.contour(xs,height,w, levels = [5,10,20])
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'condandwslice.mp4')        
        
def condavgmovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.mean(np.squeeze(fil['total_cond'].value),1))
            
        pcp = np.asarray(pcp)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "N/S Average Total Condensate (g/kg)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'condavg.mp4')

def tracermovie(maindir, modeldirs, dirout):
    print 'START'
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
	fil = hdf.File(filesrams[0], 'r')
	height = np.squeeze(fil['z_coords'].value)
	fil.close()
	filesrams = sorted(glob.glob(maindir+xdir+"/out--A*h5"))
        numfiles = len(filesrams)
	fil = hdf.File(filesrams[0], 'r')
	var1 = np.squeeze(fil['TRACERP002'].value[:,200,:])
	fil.close()
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['TRACERP002'].value[:,200,:])-var1)

        pcp = np.asarray(pcp)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs

        fig = plt.figure()
        z2 = pcp[0,:,:]

        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "center diff")

        def animate(i):
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'tracercenterdiff.mp4')

def wavgmovie(maindir, modeldirs, dirout):
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.mean(np.squeeze(fil['w'].value),1))
            
        pcp = np.asarray(pcp)
        height = np.squeeze(fil['z_coords'].value)
        xs = np.arange(pcp.shape[2])*(100./pcp.shape[2])
        ys = xs
            
        fig = plt.figure()
        z2 = pcp[0,:,:]
        
        print z2.shape, height.shape, xs.shape
        cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
        c2 = plt.colorbar(cont2,label = "N/S Average Vertical Velocity (m/s)")
        
        def animate(i): 
            z2 = pcp[i,:,:]
            cont2 = plt.contourf(xs,height,z2,levels=np.linspace(0,np.max(pcp),20))
            title='Time ' + str(i)
            return cont2

        anim = animation.FuncAnimation(fig, animate, frames=numfiles)
        anim.save(dirout+xdir+'wavg.mp4')

def compareprecip(maindir, modeldirs, dirout):
    nruns = len(modeldirs)
    allprecip = []
    
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        pcp = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            pcp.append(np.squeeze(fil['pcprate'].value))
        pcp = np.asarray(pcp)
        series = np.zeros(numfiles)
        for i in range(numfiles-1):
            series[i] = np.mean(pcp[i,:,:])
        allprecip.append(series)
    
    plt.figure()

    plt.rcParams['lines.linewidth'] = 3   
    
    for s in range(nruns):
        xs = np.arange(len(allprecip[s])) * 5
        plt.plot(xs, allprecip[s], label = modeldirs[s])
    
    plt.title('Mean Precipitation Rate')
    plt.xlabel('Minutes')
    plt.ylabel('mm/hr')
    plt.legend(loc = 'upper left')
    plt.savefig(dirout+xdir+'precipratetimeseries.png')
    plt.clf()
        
def comparemaxw(maindir, modeldirs, dirout):
    nruns = len(modeldirs)
    allmaxw = []
    
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        series = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            series.append(np.max(fil['w'].value))
        
        allmaxw.append(series)
    plt.figure()
    plt.rcParams['lines.linewidth'] = 3    
    for s in range(nruns):
        xs = np.arange(len(allmaxw[s])) * 5
        plt.plot(xs, allmaxw[s], label = modeldirs[s])
    
    plt.title('Max Vertical Velocity')
    plt.xlabel('Minutes')
    plt.ylabel('m/s')
    plt.legend(loc = 'best')
    plt.savefig(dirout+xdir+'maxwtimeseries.png')   
    plt.clf() 
    
def multifig(xdir, z2, height, varname, units, dirout):
    var = np.asarray(z2)
    if var.max() >0 or var.min() <0:
        nx = var.shape[2]
        xs = np.arange(nx)
        #levels = np.linspace(var.min(), 12, 20)  #or max(var)
        levels = np.logspace(-2,1.1,20)
        fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

        try:
            for t in range(16):
                try:
                    ax = axes.flat[t]
                    f = ax.contourf(xs, height, z2[t], levels = levels)
                    if height.max() > 20000:
                        plt.ylim(0,17000)
                    if height.max() < 50:
                        plt.ylim(0,17)
                except:
                    print 'time ', t, 'has no value in ', xdir
            cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
            cbar = plt.colorbar(f, cax=cax,**kw)
            cbar.set_label(units, rotation = 90)
            plt.suptitle(varname)
            plt.savefig(dirout+xdir+'.'+varname+'.timeseriespics.png')
            plt.close()
        except:
            print "can't plot ", xdir

def plotvertcond(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            z2.append(np.squeeze(rfile['vertint_cond'].value))
        rfile = hdf.File(filesrams[0], "r") 
        var = np.squeeze(rfile['vertint_cond'].value) 
        height = np.arange(var.shape[0])*(100./var.shape[1])
        multifig(xdir, z2, height, 'vertint_cond', 'mm', dirout) 
        
def plotmaxoverhead(maindir, modeldirs, dirout, varname, units, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile[varname].value)
            z2.append(np.max(var, 0))
        rfile = hdf.File(filesrams[0], "r")  
        var = np.squeeze(rfile[varname].value) 
        height = np.arange(var.shape[1])*(100./var.shape[1])  
        multifig(xdir, z2, height, varname + 'max', units, dirout)
                
def plotcondslice(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        for time in range(0,numfiles):
            tvar = str(time)
            if time < 10:
                tvar = '0' + tvar
            z2 = []
        
            for yval in range(134,168,2):
                rfile = hdf.File(filesrams[time], "r")
                var = np.squeeze(rfile['total_cond'].value)
                height = np.squeeze(rfile['z_coords'].value)
                ny = var.shape[2]    
                z2.append(var[:,yval,:])
            rfile = hdf.File(filesrams[0], "r")  
            height = np.squeeze(rfile['z_coords'].value)
    
            multifig(xdir, z2, height, 'smallerylog-totalcondslice_t'+tvar, 'g/kg', dirout)    

def plotwandcondoverhead(maindir, modeldirs, dirout, timediff):             
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        w2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            z2.append(np.squeeze(rfile['vertint_cond'].value))
            w2.append(np.max(np.squeeze(rfile['w'].value),0))
            
        rfile = hdf.File(filesrams[0], "r") 
        varw = np.squeeze(rfile['w'].value) 
        height = np.arange(varw.shape[1])*(100./varw.shape[1])
        
        var = np.asarray(z2)
        if var.max() >0 or var.min() <0:
            nx = var.shape[2]
            xs = np.arange(nx)
            levels = np.linspace(0, np.max(var), 20)  
            fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

            try:
                for t in range(16):
                    print np.max(z2[t])
                    
                    try:
                        ax = axes.flat[t]
                        f = ax.contourf(xs, height, z2[t], levels = levels)
                        if np.max(w2[t]) > 1:
                            g = ax.contour(xs, height, w2[t], levels = [1,30])
                        if height.max() > 20000:
                            plt.ylim(0,17000)
                        if height.max() < 50:
                            plt.ylim(0,17)
                    except:
                        print 'time ', t, 'has no value in ', xdir
                cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
                cbar = plt.colorbar(f, cax=cax,**kw)
                cbar.set_label('mm', rotation = 90)
                plt.suptitle('Total Condensate and Updraft (1,5,10,20)')
                plt.savefig(dirout+xdir+'.wandcond.timeseriespics.png')
                plt.close()
            except:
                print "can't plot ", xdir
                
             

########################################

maindir = '/nobackup/rstorer/convperts/mature/'
modeldirs = os.walk(maindir).next()[1]
modeldirs = ['aug11-control','aug17-control','feb23-control']
dirout = '/nobackup/rstorer/plots/'

#compareprecip(maindir, modeldirs, dirout)
#comparemaxw(maindir, modeldirs, dirout)

#tracermovie(maindir, modeldirs, dirout)
precipmovie(maindir, modeldirs, dirout)
#vertcondmovie(maindir, modeldirs, dirout)
#condavgmovie(maindir, modeldirs, dirout)

