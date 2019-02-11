import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar,getrho
import numpy as np

cond1 = getvar('../h5files/mature/mature-aug11-control-condensate-smoothed3km-56.h5','q')
cond2 = getvar('../h5files/mature/mature-aug11-control-condensate-smoothed3km-59.h5','q')
w = getvar('../h5files/mature/mature-aug11-control-refbudgetvars-90s-smoothed3km-56.h5','w')
precip = getvar('../h5files/mature/mature-aug11-control-precip3d-smoothed3km-56.h5','q')
rho = getrho('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5')[:,0,0]
z = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','z_coords')/1000.
pcp = getvar('../h5files/mature/mature-aug11-control-pcprate-smoothed3km-56.h5','q')
xs = np.arange(33)*3.

cmf = (cond1/1000.)*rho[:,None,None]*w
net = cmf-precip

wconv = precip/(rho[:,None,None]*(cond1/1000.))
wconv[cond1<.01]=0.

cond1=cond1*rho[:,None,None]
cond2=cond2*rho[:,None,None]

#cond1[cond1<.01]=-1
#cond2[cond2<.01]=-1

#condlevs = np.linspace(0.01,np.max(cond1),50)

fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
al = plt.contourf(xs,z,wconv[:,13,:],levels=np.linspace(np.min(wconv),np.max(wconv),50))
#bl=plt.contour(xs,z,cond1[:,13,:],levels=[0.01],linewidths=3)
cbar=plt.colorbar(al)
cbar.set_label('m/s',fontsize=20)
cbar.ax.set_yticklabels(['0','1','2','3','4','5','6','7','8','9'])
plt.title('Net Vertical Velocity',size=24)
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.savefig('level2convw-3km.pdf')
plt.clf()



condlevs = np.linspace(0.01,9.,50)

fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
plt.contourf(xs,z,cond1[:,13,:])
cbar=plt.colorbar()
cbar.set_label('g/m$^3$',fontsize=20)
cbar.ax.set_yticklabels(['0','1','2','3','4','5','6','7','8','9'])
plt.title('Condensate (t=0)',size=24)
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.savefig('level2cond1-3km.pdf')
plt.clf()

fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
plt.contourf(xs,z,cond2[:,13,:],levels=condlevs)
cbar=plt.colorbar()
cbar.set_label('g/m$^3$',fontsize=20)
cbar.ax.set_yticklabels(['0','1','2','3','4','5','6','7','8','9'])

plt.title('Condensate (t=90s)',size=24)
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.savefig('level2cond2-3km.pdf')
plt.clf()


diff = (cond2-cond1)/90.
difflevs = np.linspace(np.min(diff),np.max(diff),50)


fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
al=plt.contourf(xs,z,diff[:,13,:],levels=difflevs)
bl=plt.contour(xs,z,cond1[:,13,:],levels=[0.01],linewidths=3)
cbar=plt.colorbar(al)
cbar.set_label('g/m$^3$s',fontsize=20)
cbar.ax.set_yticklabels(['-0.012','-0.009','-0.006','-0.003','  0.0',' 0.003',' 0.006',' 0.009',' 0.012',' 0.015'])


plt.title('Condensate Difference (90s)',size=24)
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.savefig('level2diff-3km.pdf')
plt.clf()

fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
al=plt.contourf(xs,z,cmf[:,13,:],levels=np.linspace(np.min(cmf),np.max(cmf),50))
bl=plt.contour(xs,z,cond1[:,13,:],levels=[0.01],linewidths=3)
cbar=plt.colorbar(al)
cbar.set_label('kg/m$^2$s',fontsize=20)
cbar.ax.set_yticklabels(['-0.025','-0.013','  0.0',' 0.011',' 0.023',' 0.035',' 0.048',' 0.060',' 0.072',' 0.084'])

#plt.title('$\rho q_{c}w$',size=24)
plt.title('Condensate Mass Flux',size=24)
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.savefig('level2cmf-3km.pdf')
plt.clf()

fig = plt.figure()
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
plt.contourf(xs,z,net[:,13,:])
cbar=plt.colorbar()
plt.xlabel('km', size=20)
plt.ylabel('km', size=20)
plt.ylim(0,18)
plt.title('3km rho*q*w - precip term',size=24)
plt.savefig('level2net-3km.pdf')
plt.clf()

fig = plt.figure(figsize=(20,6))
plot = fig.add_subplot(111)
plot.tick_params(axis='both', which='major', labelsize=16)
plot.tick_params(axis='both', which='minor', labelsize=16)
plt.plot(xs,pcp[13,:],linewidth=3)
plt.xlabel('km', size=20)
plt.ylabel('mm/hr',size=20)
plt.title('Rain Rate',size=24)
plt.savefig('level2pcprate-3km.pdf')
plt.clf()











