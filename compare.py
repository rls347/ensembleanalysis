import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

'''A bunch of different functions to look at simulation output'''

def compareprecip(maindir, modeldirs, case, dirout):
    nruns = len(modeldirs)
    allprecip = []
    
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
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
    plt.ylabel('mm')
#    plt.legend(loc = 'upper left')
    plt.savefig(dirout+case+'compareprecipratetimeseries.png')
    plt.clf()
        
def comparemaxw(maindir, modeldirs, case, dirout):
    nruns = len(modeldirs)
    allmaxw = []
    
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/bas*h5"))
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
#    plt.legend(loc = 'upper right')
    plt.savefig(dirout+case+'comparemaxwtimeseries.png')   
    plt.clf() 
    
def multifig(xdir, z2, height, varname, dirout):
    var = np.asarray(z2)
    if var.max() >0 or var.min() <0:
        nx = var.shape[2]
        xs = np.arange(nx)
        levels = np.linspace(var.min(), var.max(), 20)
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
            plt.colorbar(f, cax=cax, **kw)
            plt.savefig(dirout+xdir+'.'+varname+'.timeseriespics.png')
            plt.close()
        except:
            print "can't plot ", xdir

def plotcondslice(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['cloud'].value+rfile['rain'].value+rfile['drizzle'].value+rfile['pristine'].value
                    +rfile['snow'].value+rfile['aggregates'].value+rfile['graupel'].value+rfile['hail'].value)
            height = np.squeeze(rfile['z_coords'].value)
            ny = var.shape[2]    
            z2.append(var[:,ny/2,:])
        rfile = hdf.File(filesrams[0], "r")  
        height = np.squeeze(rfile['z_coords'].value)
    
        multifig(xdir, z2, height, 'totalcondslice', dirout)  
        
def plotcondmax(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['cloud'].value+rfile['rain'].value+rfile['drizzle'].value+rfile['pristine'].value
                    +rfile['snow'].value+rfile['aggregates'].value+rfile['graupel'].value+rfile['hail'].value)
            height = np.squeeze(rfile['z_coords'].value)
            ny = var.shape[2]    
            z2.append(np.max(var, 1))
        print numfiles, 'WTF', maindir, xdir
        rfile = hdf.File(filesrams[0], "r")  
        height = np.squeeze(rfile['z_coords'].value)
    
        multifig(xdir, z2, height, 'totalcondmax', dirout)  
        
def plotwslice(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['w'].value)
            height = np.squeeze(rfile['z_coords'].value)
            ny = var.shape[2]    
            z2.append(var[:,ny/2,:])
        rfile = hdf.File(filesrams[0], "r")  
        height = np.squeeze(rfile['z_coords'].value)
    
        multifig(xdir, z2, height, 'wslice', dirout)  
        
def plotwmax(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['w'].value)
            height = np.squeeze(rfile['z_coords'].value)
            ny = var.shape[2]    
            z2.append(np.max(var, 1))
        rfile = hdf.File(filesrams[0], "r")  
        height = np.squeeze(rfile['z_coords'].value)
    
        multifig(xdir, z2, height, 'wmax', dirout)  
        
def plot2dvars(maindir, modeldirs, dirout, timediff, vars2d):
    for varname in vars2d:
        for xdir in modeldirs:
            filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
            numfiles = len(filesrams)
            z2 = []
            for time in range(0,numfiles,timediff):
                rfile = hdf.File(filesrams[time], "r")
                z2.append(np.squeeze(rfile[varname].value))
            rfile = hdf.File(filesrams[0], "r") 
            var = np.squeeze(rfile[varname].value) 
            height = np.arange(var.shape[0])*(100./var.shape[1])
            multifig(xdir, z2, height, varname, dirout) 

def plotwmaxoverhead(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        z2 = []
        #for time in range(40,57,timediff):
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['w'].value)
            z2.append(np.max(var, 0))
        rfile = hdf.File(filesrams[0], "r")  
        var = np.squeeze(rfile['w'].value) 
        height = np.arange(var.shape[1])*(100./var.shape[1])  
        multifig(xdir, z2, height, 'wmaxoverheadbeginning', dirout)
        
def vaporchange(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        rfile = hdf.File(filesrams[0], "r") 
        var1 = np.squeeze(rfile['vertint_vapor'].value) 
        height = np.arange(var1.shape[0])*(100./var1.shape[1])
        
        z2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            z2.append(np.squeeze(rfile['vertint_vapor'].value)-var1)

        multifig(xdir, z2, height, 'vertint_vapor_minusinitial', dirout) 

def surfacewinds(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        u2 = []
        v2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['u'].value)
            u2.append(var[1,:,:])
            var = np.squeeze(rfile['v'].value)
            v2.append(var[1,:,:])
            rfile.close()
        xs = np.arange(var.shape[1])*(100./var.shape[1])
        multifig(xdir, u2, xs, 'surfaceu', dirout)
        multifig(xdir, v2, xs, 'surfacev', dirout)
        
def surfacetemp(maindir, modeldirs, dirout, timediff):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/revu/bas*h5"))
        numfiles = len(filesrams)
        u2 = []
        for time in range(0,numfiles,timediff):
            rfile = hdf.File(filesrams[time], "r")
            var = np.squeeze(rfile['tempk'].value)
            u2.append(var[1,:,:])
            rfile.close()
        xs = np.arange(var.shape[1])*(100./var.shape[1])
        multifig(xdir, u2, xs, 'surfacetemp', dirout)
        
        
########################################
listofvars = [
    'cloud',
    'aggregates',
    'rain',
    'graupel',
    'snow',
    'drizzle',
    'pristine',
    'hail',
    'u',
    'v',
    'w',
    'tempk',
    'press',
    'theta',
    'theta_e',
    'vapor',
    'relhum',
    'latheatvapt',
    'latheatfrzt',
    'totpcp',
    'pcprate',
    'vertint_cond',
    'vertint_vapor'  ]
    
vars2d = [
    'totpcp',
    'pcprate',
    'vertint_cond',
    'vertint_vapor'  ]
    
vars3d = [
    'cloud',
    'aggregates',
    'rain',
    'graupel',
    'snow',
    'drizzle',
    'pristine',
    'hail',
    'u',
    'v',
    'w',
    'tempk',
    'press',
    'theta',
    'theta_e',
    'vapor',
    'relhum',
    'latheatvapt',
    'latheatfrzt'   ]


maindir = '/nobackup/rstorer/convperts/revu/'
#modeldirs = os.walk(maindir).next()[1]
modeldirs = ['control']
for i in range(1,25):
    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']

for case in cases:
  modeldirs = [case+'-control']
  for i in range(1,25):
    modeldirs.append(case+'-pert'+str(i))

  compareprecip(maindir, modeldirs, case, '/nobackup/rstorer/plots/')
  comparemaxw(maindir, modeldirs, case, '/nobackup/rstorer/plots/')


#plotcondslice(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#plotcondmax(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#plotwmax(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#plotwslice(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#plot2dvars(maindir, modeldirs, '/nobackup/rstorer/plots/', 3, ['pcprate','vertint_cond'])
#plotwmaxoverhead(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#vaporchange(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#surfacewinds(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)
#surfacetemp(maindir, modeldirs, '/nobackup/rstorer/plots/', 3)

