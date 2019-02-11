import matplotlib.pyplot as plt
import h5py as hdf
import numpy as np


filename =  '/nobackup/rstorer/convperts/mature-orig/feb23-control/revu/testdiams-out--AS-1999-01-26-120000-g1.h5'
fil = hdf.File(filename, 'r')

cloud = np.squeeze(fil['cloud'].value)
rain = np.squeeze(fil['rain'].value)
drizzle = np.squeeze(fil['drizzle'].value)
pristine = np.squeeze(fil['pristine'].value)
graupel = np.squeeze(fil['graupel'].value)
snow = np.squeeze(fil['snow'].value)
agg = np.squeeze(fil['aggregates'].value)
hail = np.squeeze(fil['hail'].value)

clouddiam = np.squeeze(fil['cloud_diam'].value)
raindiam = np.squeeze(fil['rain_diam'].value)
drizzlediam = np.squeeze(fil['drizzle_diam'].value)
pristinediam = np.squeeze(fil['pris_diam'].value)
graupeldiam = np.squeeze(fil['graup_diam'].value)
snowdiam = np.squeeze(fil['snow_diam'].value)
aggdiam = np.squeeze(fil['agg_diam'].value)
haildiam = np.squeeze(fil['hail_diam'].value)

height = np.squeeze(fil['z_coords'].value)

fil.close()

nz,ny,nx = cloud.shape
xs = np.arange(nx) * .25
height = height/1000.


cloud[clouddiam<.01]=np.log(0)
clouddiam[clouddiam<.01]=np.log(0)
rain[raindiam<.00001]=np.log(0)
raindiam[raindiam<.00001]=np.log(0)
drizzle[drizzlediam<.01]=np.log(0)
drizzlediam[drizzlediam<.01]=np.log(0)
pristine[pristinediam<.01]=np.log(0)
pristinediam[pristinediam<.01]=np.log(0)
snow[snowdiam<.00001]=np.log(0)
snowdiam[snowdiam<.00001]=np.log(0)
agg[aggdiam<.00001]=np.log(0)
aggdiam[aggdiam<.00001]=np.log(0)
graupel[graupeldiam<.00001]=np.log(0)
graupeldiam[graupeldiam<.00001]=np.log(0)
hail[haildiam<.00001]=np.log(0)
haildiam[haildiam<.00001]=np.log(0)

fig, axes = plt.subplots(nrows=2,ncols=2)
axq = axes[0,1].contourf(xs[160:320],height,clouddiam[:,170,160:320])
axes[0,1].set_ylim(0,20)
axes[0,1].set_title('Cloud Diameter (micron)')
plt.colorbar(axq, ax = axes[0,1])

axm =axes[0,0].contourf(xs[160:320],height,cloud[:,170,160:320])
axes[0,0].set_title('Cloud (g/kg)')
axes[0,0].set_ylim(0,20)
plt.colorbar(axm, ax = axes[0,0])

axd=axes[1,0].contourf(xs[160:320],height,pristine[:,170,160:320])
axes[1,0].set_title('Pristine (g/kg)')
axes[1,0].set_ylim(0,20)
plt.colorbar(axd, ax = axes[1,0])

axn=axes[1,1].contourf(xs[160:320],height,pristinediam[:,170,160:320])
axes[1,1].set_ylim(0,20)
axes[1,1].set_title('Pristine Diameter (micron)')
plt.colorbar(axn, ax = axes[1,1])

plt.savefig('feb23control-diameters-refcompare-cloudpris.png')
plt.clf()


fig, axes = plt.subplots(nrows=2,ncols=2)

axq = axes[0,1].contourf(xs[160:320],height,drizzlediam[:,170,160:320])
axes[0,1].set_ylim(0,20)
axes[0,1].set_title('Drizzle Diameter (micron)')
plt.colorbar(axq, ax = axes[0,1])

axm =axes[0,0].contourf(xs[160:320],height,drizzle[:,170,160:320])
axes[0,0].set_title('Drizzle (g/kg)')
axes[0,0].set_ylim(0,20)
plt.colorbar(axm, ax = axes[0,0])

axd=axes[1,0].contourf(xs[160:320],height,rain[:,170,160:320])
axes[1,0].set_title('Rain (g/kg)')
axes[1,0].set_ylim(0,20)
plt.colorbar(axd, ax = axes[1,0])

axn=axes[1,1].contourf(xs[160:320],height,raindiam[:,170,160:320])
axes[1,1].set_ylim(0,20)
axes[1,1].set_title('Rain Diameter (mm)')
plt.colorbar(axn, ax = axes[1,1])

plt.savefig('feb23control-diameters-refcompare-drizrain.png')
plt.clf()



fig, axes = plt.subplots(nrows=2,ncols=2)

axq = axes[0,1].contourf(xs[160:320],height,snowdiam[:,170,160:320])
axes[0,1].set_ylim(0,20)
axes[0,1].set_title('SnowDiameter (mm)')
plt.colorbar(axq, ax = axes[0,1])

axm =axes[0,0].contourf(xs[160:320],height,snow[:,170,160:320])
axes[0,0].set_title('Snow (g/kg)')
axes[0,0].set_ylim(0,20)
plt.colorbar(axm, ax = axes[0,0])

axd=axes[1,0].contourf(xs[160:320],height,agg[:,170,160:320])
axes[1,0].set_title('Aggregates (g/kg)')
axes[1,0].set_ylim(0,20)
plt.colorbar(axd, ax = axes[1,0])

axn=axes[1,1].contourf(xs[160:320],height,aggdiam[:,170,160:320])
axes[1,1].set_ylim(0,20)
axes[1,1].set_title('Aggregate Diameter (mm)')
plt.colorbar(axn, ax = axes[1,1])


plt.savefig('feb23control-diameters-refcompare-snowagg.png')
plt.clf()



fig, axes = plt.subplots(nrows=2,ncols=2)

axq = axes[0,1].contourf(xs[160:320],height,graupeldiam[:,170,160:320])
axes[0,1].set_ylim(0,20)
axes[0,1].set_title('Graupel Diameter (mm)')
plt.colorbar(axq, ax = axes[0,1])

axm =axes[0,0].contourf(xs[160:320],height,graupel[:,170,160:320])
axes[0,0].set_title('Graupel (g/kg)')
axes[0,0].set_ylim(0,20)
plt.colorbar(axm, ax = axes[0,0])

axd=axes[1,0].contourf(xs[160:320],height,hail[:,170,160:320])
axes[1,0].set_title('Hail (g/kg)')
axes[1,0].set_ylim(0,20)
plt.colorbar(axd, ax = axes[1,0])

axn=axes[1,1].contourf(xs[160:320],height,haildiam[:,170,160:320])
axes[1,1].set_ylim(0,20)
axes[1,1].set_title('Hail Diameter (mm)')
plt.colorbar(axn, ax = axes[1,1])

plt.savefig('feb23control-diameters-refcompare-grauphail.png')
plt.clf()






