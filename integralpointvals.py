import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

def timeseriessum(dirs, var, name,case):
	newvar = {}
	for xdir in dirs:
		print xdir, name
		x = var[xdir]
		nt,nx,ny = x.shape
		timevals = np.zeros(nt)
		for t in range(nt):
			timevals[t] = np.sum(x[t,:,:])
		plt.plot(timevals)
		newvar[xdir] = timevals
	plt.savefig('/nobackup/rstorer/plots/'+case+'-'+name+'-sum-timeseries.png')
	plt.clf()
	return newvar

def reducetomax(var, modeldirs):
	newvar = {}
	for xdir in modeldirs:
		allvar = var[xdir]
		print np.max(allvar)
		newvar[xdir] = np.max(allvar)
	return newvar

def reducetoavg(var, modeldirs):
	newvar = {}
	for xdir in modeldirs:
		allvar = var[xdir]
		print np.mean(allvar)
		newvar[xdir] = np.mean(allvar)
	return newvar

def timeseriesmmm(modeldirs, var, name):
	minvalsall = {}
	maxvalsall = {}
	meanvalsall = {}
	for xdir in modeldirs:
		print xdir, name
		x = var[xdir]
		nt,nx,ny = x.shape
		maxvals = np.zeros(nt)
		minvals = np.zeros(nt)
		meanvals = np.zeros(nt)
		xs = np.arange(nt)*5
		for t in range(nt):
			maxvals[t] = np.max(x[t,:,:])
			minvals[t] = np.min(x[t,:,:])
			meanvals[t] = np.mean(x[t,:,:])
		plt.plot(xs,maxvals)
		#plt.plot(xs,minvals)
		#plt.plot(xs,meanvals)
		minvalsall[xdir] = minvals
		maxvalsall[xdir] = maxvals
		meanvalsall[xdir] = meanvals
	outname = name.replace(".npz", "-timeseries-max.png")
	plt.savefig('/nobackup/rstorer/plots/'+outname)
	plt.clf()
	return minvalsall, maxvalsall, meanvalsall

cases = ['aug11','aug17','feb23']
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

#files = ['revu-maxw.npz','revu-maxwabove5km.npz','revu-minw.npz','revu-minwabove5km.npz']
#
#for fil in files:
#	var = np.load('/nobackup/rstorer/filesnpz/'+fil)
#	timeseriesmmm(modeldirs, var, fil)

names = ['maxw','intabove10kmice','intabove5kmcond','intabove5kmtracer2','intabove8kmliquid','intlatent',
		'maxwabove5km','intabove10kmlatent', 'intabove5kmice', 'intabove8kmcond', 'intabove8kmtracer2', 
		'intliquid','minw', 'intabove10kmliquid','intabove5kmlatent','intabove8kmice','intcond','intice',
		'inttracer2','minwabove5km', 'intabove10kmcond', 'intabove10kmtracer2', 'intabove5kmliquid', 'intabove8kmlatent']   
#names = ['echotop0','echotop5','echotop10']
names = ['intabove10kmvapor','intabove8kmvapor','intabove5kmvapor','intabove10kmtracer2','intabove8kmtracer2','intabove5kmtracer2']

for varname in names:
	for case in cases:
		modeldirs = []
		modeldirs.append(case+'-control')
		for i in range(1,25):
			modeldirs.append(case+'-pert'+str(i))
		var3d = np.load('/nobackup/rstorer/filesnpz/revu'+varname+'.npz')
		temp = timeseriessum(modeldirs, var3d, varname,case) 


#for varname in names:
#	var3d = np.load('/nobackup/rstorer/filesnpz/revu'+varname+'.npz')
	#minvals, maxvals, meanvals = timeseriesmmm(modeldirs, var3d, varname)
#	temp = timeseriessum(modeldirs, var3d, varname)
	#pointmax = reducetomax(maxvals, modeldirs)
	#pointavg = reducetoavg(meanvals, modeldirs)
	#avgname = '/nobackup/rstorer/filesnpz/revu'+varname+'avgoftime.npz'
	#maxname = '/nobackup/rstorer/filesnpz/revu'+varname+'maxoftime.npz'
	#np.savez(avgname,**pointavg)
	#np.savez(maxname,**pointmax)


	



