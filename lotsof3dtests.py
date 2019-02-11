import matplotlib 
matplotlib.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import glob
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

modeldirs = pert75()

mag = {}
for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    fil = files[0]
    p = getvar(fil,'press')
    u = getvar(fil,'u')
    v = getvar(fil,'v')
    mag[xdir] = ((u[46,10,10]-u[17,10,10])**2 + (v[46,10,10]-v[17,10,10])**2)**(.5)


cape = np.load('../filesnpz/cape_ML.npz')
rh = np.load('../filesnpz/rhlow.npz')

files = sorted(glob.glob('/nobackup/rstorer/filesnpz/*npz'))
for filename in files:
    variable = np.load(filename)
    print filename
    test = len(variable['feb23-control'].shape)

    varname = filename[27:-4]
    print varname
    if test ==0 :

        outmag = np.zeros(75)
        outrh = np.zeros(75)
        outcape = np.zeros(75)
        pcp99 = np.zeros(75)
        vert = np.zeros(75)

        for i,xdir in enumerate(modeldirs):
            outmag[i]=mag[xdir]
            outcape[i]=cape[xdir]
            outrh[i]=rh[xdir]
            vert[i] = variable[xdir]

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        p=ax.scatter3D(outrh,outcape,outmag,c=vert,depthshade=False)
        ax.set_xlabel('RH',fontweight='bold')
        ax.set_ylabel('   CAPE',fontweight='bold')
        ax.set_zlabel('Shear',fontweight='bold')
        fig.colorbar(p,shrink=.6,label=varname)
        ax.set_title(varname)
        fig.savefig('/nobackup/rstorer/plots/'+varname+'-test3dscatter-rhlow.png')
        plt.close()





