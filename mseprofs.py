import numpy as np
import copy
import h5py as hdf
import glob
import matplotlib.pyplot as plt

def getmse(mse,height):
	msesfc = mse[0]
	tmpheight = copy.deepcopy(height)
	tmpheight[height<5000]=25000
	tmpheight[mse < msesfc]=25000
	gt = np.argmin(tmpheight)
	msediff = mse[gt]-mse[gt-1]
	hdiff = height[gt]-height[gt-1]
	dmdz = msediff/hdiff
	hmse = (msesfc-mse[gt-1])/dmdz + height[gt-1]
	return msesfc,hmse

cases = ['aug17','aug11','feb23']
perts = ['-control']
for i in range(1,25):
	perts.append('-pert'+str(i))
	names = []
for case in cases:
	for i in range(25):
		names.append(case+perts[i])
for xdir in names:
	files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
	nt = len(files)

	fil = hdf.File(files[0],'r')
	temp1 = np.squeeze(fil['tempk'].value[0,1:,:,:])
	qv1 = np.squeeze(fil['vapor'].value[0,1:,:,:]) / 1000.
	height = np.squeeze(fil['z_coords'].value[1:])
	q1= qv1 / (1+qv1)
	mse1 = ((temp1*1004.) + (q1*2500000.) + (height[:,None,None]*9.8))/1000.
	fil.close()

	fil = hdf.File(files[nt-1],'r')
	temp2 = np.squeeze(fil['tempk'].value[0,1:,:,:])
	qv2 = np.squeeze(fil['vapor'].value[0,1:,:,:]) / 1000.
	q2= qv2 / (1+qv2)
	mse2 = ((temp2*1004.) + (q2*2500000.) + (height[:,None,None]*9.8))/1000.
	fil.close()

	first = np.mean(np.mean(mse1,1),1)
	last = np.mean(np.mean(mse2,1),1)

#	initmse, initlnb = getmse(mse[0,:],height)
#	endmse, endlnb = getmse(mse[1,:],height)

	initmse, initlnb = getmse(first,height)
	endmse, endlnb = getmse(last,height)

	im = np.ones(81)*initmse
	em = np.ones(81)*endmse
	il = np.ones(81)*initlnb
	el = np.ones(81)*endlnb

	plt.plot(first,height,color='blue',linewidth=3,label='Initial MSE')
	plt.plot(im,height,color = 'blue')
	plt.plot(first,il,color='blue')
	plt.plot(last,height,linewidth=3,color = 'green',label='End MSE')
	plt.plot(em,height,color = 'green')
	plt.plot(last,el,color='green')
	plt.ylim(0,18000)
	plt.xlim(320,380)
	plt.ylabel('km')
	plt.xlabel('MSE (kJ/kg)')
	plt.legend()
	plt.savefig('../plots/mse-meanprofs-'+xdir+'.png')
	plt.clf()



