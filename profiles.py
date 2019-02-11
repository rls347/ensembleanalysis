import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

'''plots an initial vertical profile in the center of the domain'''

def vertprof(maindir, modeldirs, case, outdir, varname, label, title):
    for xdir in modeldirs:
        filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
        numfiles = len(filesrams)
        print xdir
        rfile = hdf.File(filesrams[0], "r")
        var = np.squeeze(rfile[varname].value)-273.15
        height = np.squeeze(rfile['z_coords'].value)
        ny = var.shape[2]    
        z2=var[:,ny/2,ny/2]
        plt.plot(z2, height, linewidth = 3,color='lightgray')
    xdir = modeldirs[0]
    filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
    numfiles = len(filesrams)
    rfile = hdf.File(filesrams[0], "r")
    var = np.squeeze(rfile[varname].value)-273.15
    height = np.squeeze(rfile['z_coords'].value)
    ny = var.shape[2]
    z2=var[:,ny/2,ny/2]
    plt.plot(z2, height, linewidth = 3,color='red')

    plt.ylim(0,18000)
    plt.ylabel('Height (m)')
    plt.xlabel(label)    
    plt.title(title)
    plt.savefig(case+'initialtempC.png')
#    plt.savefig(outdir+case+'.'+varname+'.png')
    plt.clf()


maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = ['control']
for i in range(1,25):
    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']
case = cases[0]

outdir = '/nobackup/rstorer/plots/verticalprofiles/'

for case in cases:
  modeldirs = [case+'-control']
  for i in range(1,25):
    modeldirs.append(case+'-pert'+str(i))
    vertprof(maindir, modeldirs, case, outdir, 'tempk','Temperature (C)','Initial Temperature Profiles')
#    vertprof(maindir, modeldirs, case, outdir, 'relhum','Relative Humidity','Initial Relative Humidity Profiles')
#    vertprof(maindir, modeldirs, case, outdir, 'vapor','Vapor Mixing Ratio (g/kg)','Initial Water Vapor Profiles')


