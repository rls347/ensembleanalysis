import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

'''Code to Calculate and output ONE value for each simulation of various things'''

def totprecip(maindir, modeldirs, outfile):
    nruns = len(modeldirs)
    allprecip = {}
    
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
        fil = hdf.File(filesrams[-1], 'r')
        allprecip[xdir] = np.sum(np.squeeze(fil['totpcp'].value))
        
    np.savez(outfile, **allprecip)

        
def maxw(maindir, modeldirs, outfile):
    nruns = len(modeldirs)
    allmaxw = {}
    for xdir in modeldirs:
        print xdir
        filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
        numfiles = len(filesrams)
        series = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            series.append(np.max(fil['w'].value))
        
        allmaxw[xdir] = np.max(series)
    np.savez(outfile, **allmaxw)

def ltss(maindir, modeldirs, outfile):
	allstab = {}
	for xdir in modeldirs:
		print 'ltss', xdir
		filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
		fil = hdf.File(filesrams[0],'r')
		theta = np.asarray(fil['theta'].value[0,:,20,20])
		lts = theta[29]-theta[1]
		allstab[xdir]=lts
		print lts
	np.savez(outfile,**allstab)

def meandiam(maindir, modeldirs):
	vars = ['cloud','rain','drizzle','pristine','snow','aggregates','graupel','hail']
	alldiams = {}
	for xdir in modeldirs:
		alldiams[xdir]={}
		for var in vars:
			alldiams[xdir][var] = np.zeros(60)
	for xdir in modeldirs:
		print 'diam',xdir
		filesrams = sorted(glob.glob(maindir+xdir+"-*h5"))
		for t in range(len(filesrams)):
			fil = hdf.File(filesrams[t],'r')
			for var in vars:
				x = np.asarray(fil[var].value)
				x = x[x>0]
				alldiams[xdir][var][t] = np.mean(x)
	for var in vars:
		onediam = {}
		for xdir in modeldirs:
			onediam[xdir] = np.mean(alldiams[xdir][var])
		outfile = '../filesnpz/maturediam'+var+'.npz'
		np.savez(outfile, **onediam)
				
def reducetomax(var, modeldirs):
	newvar = {}
	for xdir in modeldirs:
		allvar = var[xdir]
		newvar[xdir] = np.max(allvar)
	return newvar

def reducetosum(var, modeldirs):
	newvar = {}
	for xdir in modeldirs:
		allvar = var[xdir]
		newvar[xdir] = np.sum(allvar)

    
cases = ['aug11','aug17','feb23']    
maindir = '/nobackup/rstorer/convperts/revu/'        
modeldirs = []
for case in cases:
  modeldirs.append(case+'-control')
  for i in range(1,25):
    modeldirs.append(case+'-pert'+str(i))

#totprecip(maindir, modeldirs,'totpcppoints.npz')
#maxw(maindir, modeldirs, 'maxwpoints.npz')
#totprecip(maindir,modeldirs,'maturetotpcppoints.npz')
#maxw(maindir, modeldirs, 'maturemaxwpoints.npz')

#meandiam('/nobackup/rstorer/convperts/diam/',modeldirs)
ltss(maindir, modeldirs, 'ltss.npz')

 
    
