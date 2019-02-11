import numpy as np
import matplotlib.pyplot as plt

cases = ['aug11','aug17','feb23']
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

height = np.load('../filesnpz/height.npy')
allcloudtops = np.load('../filesnpz/cloudtops.npz')
allmaxw = np.load('../filesnpz/revu-maxw.npz')
allminw = np.load('../filesnpz/revu-minw.npz')
allpcprate = np.load('../filesnpz/allpcprates.npz')
allconvrate = np.load('../filesnpz/allconvrates.npz')

for xdir in modeldirs:
	cloudtops = allcloudtops[xdir]
	maxw = allmaxw[xdir]
	minw = allminw[xdir]
	pcprate = allpcprate[xdir]
	convrate = allconvrate[xdir]


	nt,nx,nz = cloudtops.shape
	xs = np.arange(nt)*5

	timct = np.max(np.max(cloudtops,1),1) / np.max(cloudtops)
	timxw = np.max(np.max(maxw,1),1) / np.max(maxw)
	timnw = np.min(np.min(minw,1),1) / np.min(minw)
	timpcp = np.sum(np.sum(pcprate,1),1) / np.sum(pcprate)
	timconv = np.sum(np.sum(convrate,1),1) / np.sum(convrate)
	timfrac = np.zeros(nt)
	for t in range(nt):
		if timpcp[t] >0:
			timfrac[t] = (timconv[t]/timpcp[t]) * (np.sum(convrate)/np.sum(pcprate))

	plt.plot(xs, timct, linewidth = 2, label = 'cloudtop')
	plt.plot(xs, timxw, linewidth = 2, label = 'max w')
	plt.plot(xs, timnw, linewidth = 2, label = 'min w')
	plt.plot(xs, timpcp, linewidth = 2, label = 'precip')
	plt.plot(xs, timconv, linewidth = 2, label = 'conv precip')
	plt.plot(xs, timfrac, linewidth = 2, label = 'pcp fraction')
	plt.legend()
	plt.xlabel('minutes')
	plt.ylabel('fraction of max')
	plt.title(xdir)
	plt.savefig('/nobackup/rstorer/plots/timemetrics-'+xdir+'.png')
	plt.clf()


