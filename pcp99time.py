import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import copy
from matplotlib import rc

allrates = np.load('/nobackup/rstorer/filesnpz/allpcprates.npz')
allmaxw = np.load('/nobackup/rstorer/filesnpz/revumaxw.npz')

cases = ['aug17','aug11','feb23']
perts = ['-control']
for i in range(1,25):
	perts.append('-pert'+str(i))
names = []
for case in cases:
	for i in range(25):
		names.append(case+perts[i])

maxw = [] 
rate99 = [] 

for x,case in enumerate(cases):
	maxw.append([])
	rate99.append([])
	for i in range(25):
		name = case+perts[i]
		ws = allmaxw[name]
		rates = allrates[name]
		nt,nx,ny = rates.shape
		maxw[x].append(np.zeros(nt))
		rate99[x].append(np.zeros(nt))
		for t in range(nt):
			pcprate = rates[t,:,:]
			mw = ws[t,:,:]
			rate99[x][i][t] = np.percentile(pcprate,99)
			maxw[x][i][t] = np.max(mw)



#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
xa17=np.asarray(maxw[0])
xa11=np.asarray(maxw[1])
xf23=np.asarray(maxw[2])
ya17=np.asarray(rate99[0])
ya11=np.asarray(rate99[1])
yf23=np.asarray(rate99[2])
fig = plt.figure(figsize=(10,8))
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=20)
plot.tick_params(axis='both', which='minor', labelsize=20)
plt.scatter(xa17,ya17,color = 'c',label = 'Aug 17')
plt.scatter(xa11,ya11,color = 'm',label = 'Aug 11')
plt.scatter(xf23,yf23,color = 'y',label = 'Feb 23')
plt.legend(loc='upper left',fontsize=20)
plt.xlabel('Max Updraft (m/s)', size=22,fontweight='normal')
plt.ylabel('99th % Rain Rate (mm/hr)', size=22,fontweight='normal')
plt.title('Max Storm Updraft vs Extreme Precipitation',size=24,fontweight='normal')
plt.savefig('maxwvs99preciptimes.png',dpi=300)
plt.clf()




