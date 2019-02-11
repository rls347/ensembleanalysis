import numpy as np
import h5py as hdf
import atmos
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import os



def makefile(infile,outfilename):    
    rfile = hdf.File(infile, 'r')
    heights = rfile['z_coords'].value[1:]
    tempk = np.zeros_like(heights)
    press = np.zeros_like(heights)
    vapor = np.zeros_like(heights)
    for i in range(len(heights)):
        tempk[i] = np.mean(rfile['tempk'].value[0,i+1,:,:])
        press[i] = np.mean(rfile['press'].value[0,i+1,:,:])
        vapor[i] = np.mean(rfile['vapor'].value[0,i+1,:,:])

    rho = (press*100.)/ (287.*tempk)

    relhum = rfile['relhum'].value[0,1:,0,0]
    u = rfile['u'].value[0,1:,0,0]
    v = rfile['v'].value[0,1:,0,0]

    data = {'T':tempk, 'RH':relhum, 'p':press*100.}
    dewpt = atmos.calculate('Td', **data)
    
    sat = atmos.calculate('rvs', **data) * 1000.
    
    dz = np.zeros_like(heights)
    dz[0:-1] = np.diff(heights)
    dz[-1] = dz[-2]
    
    vsat = sat * rho * dz
    vact = vapor * rho * dz
    
    lows = np.where(press > 850.)
    mids = np.logical_and(press < 850, press > 500)
    highs = np.where(press < 500)
    
    lowsat = 100. * (np.sum(vact[lows]) / np.sum(vsat[lows]))
    midsat = 100. * (np.sum(vact[mids]) / np.sum(vsat[mids]))
    highsat = 100. * (np.sum(vact[highs]) / np.sum(vsat[highs]))
    
    print outfilename
    print lowsat, midsat, highsat
    print ' ' 
    
    outfile = Dataset(outfilename, "w", format="NETCDF4")
    height = outfile.createDimension("height", len(heights))
    dim = outfile.createVariable('height',"f4",('height'))
    outfile.variables['height'][:]=heights
    a = outfile.createVariable('temp',"f4",('height'))
    outfile.variables['temp'][:]=tempk-273.15
    aa = outfile.createVariable('press',"f4",('height'))
    outfile.variables['press'][:]=press
    a = outfile.createVariable('dewpoint',"f4",('height'))
    outfile.variables['dewpoint'][:]=dewpt-273.15
    a = outfile.createVariable('v',"f4",('height'))
    outfile.variables['v'][:]=v
    a = outfile.createVariable('u',"f4",('height'))
    outfile.variables['u'][:]=u
    outfile.close()

maindir = '/nobackup/rstorer/convperts/revu'
modeldirs = os.walk(maindir).next()[1] 

for dir in modeldirs:
    infile = maindir+'/'+dir+'/basic001-out--AS-1999-01-26-120000-g1.h5'
    outfile = dir + '.nc'
    makefile(infile,outfile)
