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



plt.contourf(xs[160:320], height, micro2[:,170,160:320])
plt.ylim(0,18000)
plt.ylabel('height')
plt.xlabel('km')
plt.title('microphysics')
plt.colorbar()
plt.savefig(outdir+'micro.png')
plt.clf()

diff = cond2-cond1
plt.contourf(xs[160:320], height, diff[:,170,160:320])
plt.ylim(0,18000)
plt.ylabel('height')
plt.xlabel('km')
plt.title('Condensate Difference')
plt.colorbar()
plt.savefig(outdir+'conddiff.png')
plt.clf()



