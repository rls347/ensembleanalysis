import numpy as np
import matplotlib.pyplot as plt
import copy

allrates = np.load('/nobackup/rstorer/filesnpz/allpcprates.npz')
allmaxw = np.load('/nobackup/rstorer/filesnpz/revumaxw.npz')
allmaxw5 = np.load('/nobackup/rstorer/filesnpz/revumaxwabove5km.npz')

cases = ['aug17','aug11','feb23']
perts = ['-control']
for i in range(1,25):
	perts.append('-pert'+str(i))
names = []
for case in cases:
	for i in range(25):
		names.append(case+perts[i])

maxw = np.zeros(75)
maxw5 = np.zeros(75)
meanrate = np.zeros(75)
rate90 = np.zeros(75)
rate95 = np.zeros(75)
rate99 = np.zeros(75)
totpcp = np.zeros(75)
totconv = np.zeros(75)
numconv = np.zeros(75)
frac = np.zeros(75)

for i, name in enumerate(names):
	ws = allmaxw[name]
	ws5 = allmaxw5[name]
	maxw[i] = np.max(ws)
	maxw5[i] = np.max(ws5)
	pcprate = allrates[name]
	meanrate[i] = np.mean(pcprate)
	rate90[i] = np.percentile(pcprate,90)
	rate95[i] = np.percentile(pcprate,95)
	rate99[i] = np.percentile(pcprate,99)
	totpcp[i] = np.sum(pcprate)*(5./60)
	cpcp = copy.deepcopy(pcprate)
	cpcp[pcprate<25.4]=0.0
	totconv[i] = np.sum(cpcp)*(5./60)
	cpcp[cpcp>0] = 1
	numconv[i] = np.sum(cpcp) * (.25*.25) /(100*100)
	frac[i] = totconv[i]/totpcp[i]


plt.scatter(maxw,meanrate)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('Mean Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw-meanrate.png')
plt.clf()

plt.scatter(maxw,rate90)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('90th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw-rate90.png')
plt.clf()

plt.scatter(maxw,rate95)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('95th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw-rate95.png')
plt.clf()

plt.scatter(maxw,rate99)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('99th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw-rate99.png')
plt.clf()

plt.scatter(maxw,totpcp)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('Total Precipitation (mm)')
plt.savefig('pstats-maxw-totpcp.png')
plt.clf()

plt.scatter(maxw,totconv)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('Total Convective Precipitation (mm)')
plt.savefig('pstats-maxw-totconv.png')
plt.clf()

plt.scatter(maxw,numconv)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('Convective Precipitation Area (km2)')
plt.savefig('pstats-maxw-numconv.png')
plt.clf()

plt.scatter(maxw,frac)
plt.xlabel('Max Vertical Velocity (m/s)')
plt.ylabel('Convective Precipitation Fraction')
plt.savefig('pstats-maxw-frac.png')
plt.clf()

plt.scatter(maxw5,meanrate)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('Mean Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw5-meanrate.png')
plt.clf()

plt.scatter(maxw5,rate90)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('90th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw5-rate90.png')
plt.clf()

plt.scatter(maxw5,rate95)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('95th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw5-rate95.png')
plt.clf()

plt.scatter(maxw5,rate99)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('99th Percentile Precipitation Rate (mm/hr)')
plt.savefig('pstats-maxw5-rate99.png')
plt.clf()

plt.scatter(maxw5,totpcp)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('Total Precipitation (mm)')
plt.savefig('pstats-maxw5-totpcp.png')
plt.clf()

plt.scatter(maxw5,totconv)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('Total Convective Precipitation (mm)')
plt.savefig('pstats-maxw5-totconv.png')
plt.clf()

plt.scatter(maxw5,numconv)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('Convective Precipitation Area (km2)')
plt.savefig('pstats-maxw5-numconv.png')
plt.clf()

plt.scatter(maxw5,frac)
plt.xlabel('Max Vertical Velocity Above 5km (m/s)')
plt.ylabel('Convective Precipitation Fraction')
plt.savefig('pstats-maxw5-frac.png')
plt.clf()


xa17=maxw[0:25]
xa11=maxw[25:50]
xf23=maxw[50:] 
ya17=rate99[0:25]
ya11=rate99[25:50]
yf23=rate99[50:]
plt.scatter(xa17,ya17,color = 'c',s=50,label = 'Aug 17')
plt.scatter(xa11,ya11,color = 'm',s=50,label = 'Aug 11')
plt.scatter(xf23,yf23,color = 'y',s=50,label = 'Feb 23')
plt.legend(loc='upper left')
plt.xlabel('Max Vertical Velocity (m/s)', size=16)
plt.ylabel('99th Percentile Precipitation Rate (mm/hr)', size=16)
plt.title('Max Storm Updraft vs Extreme Precipitation',size=20)
plt.savefig('maxwvs99precip.png')
plt.clf()




