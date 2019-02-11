import matplotlib
import os
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar
import glob
from rachelutils.hdfload import getdz

def makeoneplot(i,fil1,fil2,yval):
    outdir = '/nobackup/rstorer/plots/budgetslices/'

    cond1 = getvar(fil1, 'total_cond')/1000.
    cond2 = getvar(fil2, 'total_cond')/1000.
    micro2 = (getvar(fil2, 'nuccldrt') + getvar(fil2, 'nucicert') + getvar(fil2, 'vapliqt') + getvar(fil2, 'vapicet'))/1000.
    diff = cond2-cond1
    height = getvar(fil1, 'z_coords')
    xs = np.arange(400)*.25
    dz = getdz(fil1)

    plt.subplot(2,1,1)
    plt.contourf(xs[160:320], height, diff[:,yval,160:320])
    plt.ylim(0,18000)
    plt.ylabel('height')
    plt.title('Condensate Difference')
    plt.colorbar()

    plt.subplot(2,1,2)
    plt.contourf(xs[160:320], height, micro2[:,yval,160:320])
    plt.ylim(0,18000)
    plt.ylabel('height')
    plt.title('microphysics')
    plt.colorbar()

    plt.savefig(outdir+'time_'+i+'_y'+str(yval)+'.png')
    plt.clf()



files = sorted(glob.glob('/nobackup/rstorer/convperts/mature/feb23-control/feb*h5'))
nfiles = len(files)
for y in range(140,200,2):
    for time in range(1,nfiles-1):
        ivar = str(time)
        if time<10:
            ivar = '0'+ivar
        makeoneplot(ivar,files[time],files[time+1],y)

    os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/budgetslices/time_*"+str(y)+".png' -c:v libx264 -pix_fmt yuv420p ../plots/budgetslices/budgetmovie"+str(y)+".mp4")
    os.system("rm ../plots/budgetslices/time_*png")
