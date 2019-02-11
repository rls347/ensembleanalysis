import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
import glob
import os

cases = ['aug11','aug17','feb23']
maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))
dirsdirs = []
dirsdirs.append('control')
for i in range(1,25):
	dirsdirs.append('pert'+str(i))

hdffil = '../convperts/revu/feb23-control/basic001-out--AS-1999-01-26-120000-g1.h5'
hf = hdf.File(hdffil, 'r')
height = hf['z_coords'].value
hf.close()

dz = np.zeros_like(height)
dz[0:-1] = np.diff(height)
dz[-1]=dz[-2]
dz = dz * 100


aug11tracers = np.load('../filesnpz/aug11-2dtracer2int.npz')
aug17tracers = np.load('../filesnpz/aug17-2dtracer2int.npz')
feb23tracers = np.load('../filesnpz/feb23-2dtracer2int.npz')

totmax = {}
int8max = {}
int12max = {}

for xdir in dirsdirs:
	aug11all = aug11tracers[xdir] * dz[None,:]
	aug17all = aug17tracers[xdir] * dz[None,:]
	feb23all = feb23tracers[xdir] * dz[None,:]

	a11totint = np.sum(aug11all,1)
	a17totint = np.sum(aug17all,1)
	f23totint = np.sum(feb23all,1)

	xsa11 = np.arange(len(a11totint))*5
	xsa17 = np.arange(len(a17totint))*5
	xsf23 = np.arange(len(f23totint))*5
	plt.plot(xsa11, a11totint, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Total Vertical Integral Tracer 2')
	plt.savefig('../plots/tracer2totinttimeseries.aug11-'+xdir+'.png')
	plt.clf()

	plt.plot(xsa17, a17totint, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Total Vertical Integral Tracer 2')
	plt.savefig('../plots/tracer2totinttimeseries.aug17-'+xdir+'.png')
	plt.clf()

	plt.plot(xsf23, f23totint, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Total Vertical Integral Tracer 2')
	plt.savefig('../plots/tracer2totinttimeseries.feb23-'+xdir+'.png')
	plt.clf()

	a11int8 = np.sum(aug11all[:,height>8000],1)
	a17int8 = np.sum(aug17all[:,height>8000],1)
	f23int8 = np.sum(feb23all[:,height>8000],1)
	
	plt.plot(xsa11, a11int8, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 8 km Tracer 2')
	plt.savefig('../plots/tracer2int8timeseries.aug11-'+xdir+'.png')
	plt.clf()

	plt.plot(xsa17, a17int8, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 8km Tracer 2')
	plt.savefig('../plots/tracer2int8timeseries.aug17-'+xdir+'.png')
	plt.clf()

	plt.plot(xsf23, f23int8, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 8km Tracer 2')
	plt.savefig('../plots/tracer2int8timeseries.feb23-'+xdir+'.png')
	plt.clf()
	
	a11int12 = np.sum(aug11all[:,height>12000],1)
	a17int12 = np.sum(aug17all[:,height>12000],1)
	f23int12 = np.sum(feb23all[:,height>12000],1)

	plt.plot(xsa11, a11int12, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 12km Tracer 2')
	plt.savefig('../plots/tracer2int12timeseries.aug11-'+xdir+'.png')
	plt.clf()

	plt.plot(xsa17, a17int12, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 12km Tracer 2')
	plt.savefig('../plots/tracer2int12timeseries.aug17-'+xdir+'.png')
	plt.clf()

	plt.plot(xsf23, f23int12, linewidth = 3)
	plt.xlabel('Time (min)')
	plt.ylabel('Vertical Integral Above 12km Tracer 2')
	plt.savefig('../plots/tracer2int12timeseries.feb23-'+xdir+'.png')
	plt.clf()

	lbla11 = 'aug11-'+xdir
	lbla17 = 'aug17-'+xdir
	lblf23 = 'feb23-'+xdir

	totmax[lbla11] = np.max(a11totint)
	totmax[lbla17] = np.max(a17totint)
	totmax[lblf23] = np.max(f23totint)

	int8max[lbla11] = np.max(a11int8)
	int8max[lbla17] = np.max(a17int8)
	int8max[lblf23] = np.max(f23int8)

	int12max[lbla11] = np.max(a11int12)
	int12max[lbla17] = np.max(a17int12)
	int12max[lblf23] = np.max(f23int12)


np.savez('tracer2_max_totint.npz', **totmax)
np.savez('tracer2_max_int8.npz', **int8max)
np.savez('tracer2_max_int12.npz', **int12max)



