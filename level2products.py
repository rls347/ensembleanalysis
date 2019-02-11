import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar,getrho
import numpy as np

cond1 = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','total_cond')/1000.
cond2 = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-060.h5','total_cond')/1000.
w = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','w')
precip = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','precip3d')
rho = getrho('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5')
z = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','z_coords')
pcp = getvar('/nobackup/rstorer/convperts/mature/aug11-control/aug11-control-mature-057.h5','pcprate')
xs = np.arange(400)*.25

cmf = cond1*rho*w
net = cmf-precip

cond1=cond1*1000.*rho
cond2=cond2*1000.*rho

cond1[cond1<.01]=-1
cond2[cond2<.01]=-1

condlevs = np.linspace(0,np.max(cond1),50)

plt.contourf(xs,z,cond1[:,168,:],levels=condlevs)
plt.colorbar()
plt.title('cond time 1')
plt.savefig('level2cond1.pdf')
plt.clf()

plt.contourf(xs,z,cond2[:,168,:],levels=condlevs)
plt.colorbar()
plt.title('cond +90s')
plt.savefig('level2cond2.pdf')
plt.clf()

diff = (cond2-cond1)/90.

plt.contourf(xs,z,diff[:,168,:])
plt.colorbar()
plt.title('cond diff 90s')
plt.savefig('level2diff.pdf')
plt.clf()

plt.contourf(xs,z,cmf[:,168,:])
plt.colorbar()
plt.title('rho*q*w')
plt.savefig('level2cmf.pdf')
plt.clf()

plt.contourf(xs,z,net[:,168,:])
plt.colorbar()
plt.title('rho*q*w - precip term')
plt.savefig('level2net.pdf')
plt.clf()

plt.plot(xs,pcp[168,:])
plt.title('precip rate')
plt.savefig('level2pcprate.pdf')
plt.clf()











print z
