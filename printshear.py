import matplotlib 
matplotlib.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import glob
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

modeldirs = pert75()

#mag = {}
#for xdir in modeldirs:
#    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
#    fil = files[0]
#    p = getvar(fil,'press')
#    u = getvar(fil,'u')
#    v = getvar(fil,'v')
#    mag[xdir] = ((u[46,10,10]-u[17,10,10])**2 + (v[46,10,10]-v[17,10,10])**2)**(.5)

#np.savez('../filesnpz/shear.npz',**mag)
mag = np.load('../filesnpz/shear.npz')
cape = np.load('../filesnpz/cape_ML.npz')
rh = np.load('../filesnpz/rhlow.npz')
w = np.load('../filesnpz/maxwpoints.npz')
allrates = np.load('../filesnpz/allpcprates.npz')
vertical = np.load('../filesnpz/budgetintegral-growing-vertical.npz')
vapor = np.load('colvap-press-1000-100.npz')
totpcp = np.load('totpcpmm.npz')
allw99 = np.load('w99.npz')

outmag = np.zeros(75)
outrh = np.zeros(75)
outcape = np.zeros(75)
maxw = np.zeros(75)
pcp99 = np.zeros(75)
vert = np.zeros(75)
outvap = np.zeros(75)
outpcp = np.zeros(75)
w99 = np.zeros(75)

for i,xdir in enumerate(modeldirs):
    outmag[i]=mag[xdir]
    outcape[i]=cape[xdir]
    outrh[i]=rh[xdir]
    maxw[i]=w[xdir]
    allpcp = allrates[xdir]
    allpcp = allpcp[allpcp>0]
    pcp99[i] = np.percentile(allpcp,99)
    vert[i] = vertical[xdir]
    outvap[i] = vapor[xdir]
    outpcp[i] = totpcp[xdir]
    w99[i] = allw99[xdir]


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(outvap[0:24],outcape[0:24],outmag[0:24],color='m',depthshade=False,label = 'Aug 11')
ax.scatter3D(outvap[25:49],outcape[25:49],outmag[25:49],color='c',depthshade=False,label = 'Aug 17')
ax.scatter3D(outvap[50:74],outcape[50:74],outmag[50:74],color='y',depthshade=False,label = 'Feb 23')
ax.legend(loc='best')
ax.set_xlabel('PWAT',fontweight='bold')
ax.set_ylabel('   CAPE',fontweight='bold')
ax.set_zlabel('Shear',fontweight='bold')
ax.set_title('Model Environments   \n',fontweight='bold',size=20)
fig.savefig('test3dscatter-colvap.png')
plt.close()



#fig = plt.figure()
#ax = plt.axes(projection='3d')
#p=ax.scatter3D(outrh,outcape,outmag,c=maxw,depthshade=False)
#ax.set_xlabel('RH',fontweight='bold')
#ax.set_ylabel('   CAPE',fontweight='bold')
#ax.set_zlabel('Shear',fontweight='bold')
#fig.colorbar(p,shrink=.6,label='Max W')
#fig.savefig('maxwcolor-test3dscatter.png')
#plt.close()
#
#
#fig = plt.figure()
#ax = plt.axes(projection='3d')
#p=ax.scatter3D(outrh,outcape,outmag,c=vert,depthshade=False)
#ax.set_xlabel('RH',fontweight='bold')
#ax.set_ylabel('   CAPE',fontweight='bold')
#ax.set_zlabel('Shear',fontweight='bold')
#fig.colorbar(p,shrink=.6,label='Max W')
#fig.savefig('vertfluxcolor-test3dscatter.png')
#plt.close()
#
#fig = plt.figure()
#ax = plt.axes(projection='3d')
#p=ax.scatter3D(outrh,outcape,outmag,c=pcp99,depthshade=False)
#ax.set_xlabel('RH',fontweight='bold')
#ax.set_ylabel('   CAPE',fontweight='bold')
#ax.set_zlabel('Shear',fontweight='bold')
#fig.colorbar(p,shrink=.6,label='99th % Precip Rate')
#fig.savefig('pcp99color-pcpgt0only-test3dscatter.png')
#plt.close()
#
#plt.scatter(outrh,pcp99)
#plt.savefig('not3dscatter-rh-pcp99.png')
#plt.close()
#
#plt.scatter(outmag,pcp99)
#plt.savefig('not3dscatter-shear-pcp99.png')
#plt.close()
#
#plt.scatter(outcape,pcp99)
#plt.savefig('not3dscatter-cape-pcp99.png')
#plt.close()
#
#plt.scatter(outrh,maxw)
#plt.savefig('not3dscatter-rh-maxw.png')
#plt.close()
#
#plt.scatter(outmag,maxw)
#plt.savefig('not3dscatter-shear-maxw.png')
#plt.close()
#
#plt.scatter(outcape,maxw)
#plt.savefig('not3dscatter-cape-maxw.png')
#plt.close()
#
xlabels = np.linspace(50,58,9,dtype=int)
ylabels = np.linspace(0,4000,9,dtype = int)
zlabels = np.linspace(8,17,10,dtype = int)

fig = plt.figure(figsize=(10,4.5)) 
ax = fig.add_subplot(1,2,1, projection = '3d')
p=ax.scatter3D(outvap,outcape,outmag,c=maxw,depthshade=False)
ax.set_xlabel('PWAT')
ax.set_ylabel('   CAPE')
ax.set_zlabel('Shear')
ax.set_title('Max Updraft')
ax.set_xticklabels(xlabels, fontsize = 10)
ax.set_yticklabels(ylabels, fontsize = 10)
ax.set_zticklabels(zlabels, fontsize = 10)
cbar = fig.colorbar(p,shrink=.6)
cbar.ax.set_ylabel('m/s',rotation=90)

ax2 = fig.add_subplot(1,2,2, projection='3d')
p2=ax2.scatter3D(outvap,outcape,outmag,c=pcp99,depthshade=False)
ax2.set_xlabel('PWAT')
ax2.set_ylabel('   CAPE')
ax2.set_zlabel('Shear')
ax2.set_title('99th Percentile Rain Rate')
ax2.set_xticklabels(xlabels, fontsize = 10)
ax2.set_yticklabels(ylabels, fontsize = 10)
ax2.set_zticklabels(zlabels, fontsize = 10)
cbar2 = fig.colorbar(p2,shrink=.6)
cbar2.ax.set_ylabel('mm/hr',rotation=90)

plt.tight_layout()
fig.savefig('scatter3d-maxw-pcp99-changerhtopway.png')
plt.close(fig)



fig = plt.figure(figsize=(10,4.5))
ax = fig.add_subplot(1,2,1, projection = '3d')
p=ax.scatter3D(outvap,outcape,outmag,c=outpcp,depthshade=False)
ax.set_xlabel('PWAT')
ax.set_ylabel('   CAPE')
ax.set_zlabel('Shear')
ax.set_title('Total Precip')
ax.set_xticklabels(xlabels, fontsize = 10)
ax.set_yticklabels(ylabels, fontsize = 10)
ax.set_zticklabels(zlabels, fontsize = 10)
cbar = fig.colorbar(p,shrink=.6)
cbar.ax.set_ylabel('mm',rotation=90)

ax2 = fig.add_subplot(1,2,2, projection='3d')
p2=ax2.scatter3D(outvap,outcape,outmag,c=w99,depthshade=False)
ax2.set_xlabel('PWAT')
ax2.set_ylabel('   CAPE')
ax2.set_zlabel('Shear')
ax2.set_title('99th Percentile Vertical Velocity')
ax2.set_xticklabels(xlabels, fontsize = 10)
ax2.set_yticklabels(ylabels, fontsize = 10)
ax2.set_zticklabels(zlabels, fontsize = 10)
cbar2 = fig.colorbar(p2,shrink=.6)
cbar2.ax.set_ylabel('m/s',rotation=90)

plt.tight_layout()
fig.savefig('scatter3d-w99-totpcp-changerhtopway.png')
plt.close()






print xlabels
print outvap
