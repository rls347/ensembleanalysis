import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar
import glob
from rachelutils.hdfload import getdz

files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/feb*h5'))
fil1 = hdf.File(files[1],'r')
fil2 = hdf.File(files[2],'r')

outdir = '/nobackup/rstorer/plots/budgetslices/'

cond1 = getvar(fil1, 'total_cond')/1000.
cond2 = getvar(fil2, 'total_cond')/1000.
rho1 = (getvar(fil1, 'press') * 100.) / (getvar(fil1, 'tempk') *287.)
rho2 = (getvar(fil2, 'press') * 100.) / (getvar(fil2, 'tempk') *287.)
w1 = getvar(fil1, 'w')
w2 = getvar(fil2, 'w')
micro1 = (getvar(fil1, 'nuccldrt') + getvar(fil1, 'nucicert') + getvar(fil1, 'vapliqt') + getvar(fil1, 'vapicet'))/1000.
micro2 = (getvar(fil2, 'nuccldrt') + getvar(fil2, 'nucicert') + getvar(fil2, 'vapliqt') + getvar(fil2, 'vapicet'))/1000.
pcp1 = getvar(fil1, 'precip3d')
pcp2 = getvar(fil2, 'precip3d')

height = getvar(fil1, 'z_coords')
xs = np.arange(400)*.25
dz = getdz(fil1)


#micro1=micro1*rho1*dz[:,None,None]/30.
#micro2 = micro2*rho2*dz[:,None,None]/30.

#plt.contourf(xs[160:320], height, cond1[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('Condensate Time 1')
#plt.colorbar()
#plt.savefig(outdir+'cond1.png')
#plt.clf()
#
#plt.contourf(xs[160:320], height, cond2[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.colorbar()
#plt.xlabel('km')
#plt.title('Condensate Time 2 (30s)')
#plt.savefig(outdir+'cond2.png')
#plt.clf()
#
#massflux2 = cond2*rho2*w2
#plt.contourf(xs[160:320], height, massflux2[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('mass flux 2')
#plt.colorbar()
#plt.savefig(outdir+'massflux2.png')
#plt.clf()
#
#
#massflux1 = cond1*rho1*w1
#plt.contourf(xs[160:320], height, massflux1[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('mass flux 1')
#plt.colorbar()
#plt.savefig(outdir+'massflux1.png')
#plt.clf()
#
#plt.contourf(xs[160:320], height, pcp2[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('precip flux 2')
#plt.colorbar()
#plt.savefig(outdir+'pcp2.png')
#plt.clf()
#
#
#plt.contourf(xs[160:320], height, pcp1[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('precip flux 1')
#plt.colorbar()
#plt.savefig(outdir+'pcp1.png')
#plt.clf()


plt.contourf(xs[160:320], height, micro2[:,170,160:320])
plt.ylim(0,18000)
plt.ylabel('height')
plt.xlabel('km')
plt.title('microphysics')
plt.colorbar()
plt.savefig(outdir+'micro.png')
plt.clf()

#diff = ((cond2*rho2*dz[:,None,None])-(cond1*rho1*dz[:,None,None]))/30.
diff = cond2-cond1
plt.contourf(xs[160:320], height, diff[:,170,160:320])
plt.ylim(0,18000)
plt.ylabel('height')
plt.xlabel('km')
plt.title('Condensate Difference')
plt.colorbar()
plt.savefig(outdir+'conddiff.png')
plt.clf()

#
#vert1 = massflux1-pcp1
#vert2 = massflux2-pcp2
#
#plt.contourf(xs[160:320], height, vert1[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('net vertical flux 1')
#plt.colorbar()
#plt.savefig(outdir+'vert1.png')
#plt.clf()
#
#plt.contourf(xs[160:320], height, vert2[:,170,160:320])
#plt.ylim(0,18000)
#plt.ylabel('height')
#plt.xlabel('km')
#plt.title('net vertical flux 2')
#plt.colorbar()
#plt.savefig(outdir+'vert2.png')
#plt.clf()


