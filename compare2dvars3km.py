import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import h5py as hdf
from rachelutils.hdfload import getvar,getrho
from rachelutils.dumbnaming import pert75
import glob


modeldirs = pert75()
times = ['mature','growing']
height = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','z_coords')

#varlist = ['height0db','height5db','height10db','height20db','delheight0db','delheight5db','delheight10db','delheight20db','w0db','w5db','w10db','w20db','dryflux0db','dryflux5db','dryflux10db','dryflux20db','vaporflux0db','vaporflux5db','vaporflux10db','vaporflux20db','netcondflux0db','netcondflux5db','netcondflux10db','netcondflux20db','delz5km','delz8km','delz10km','w5km','w8km','w10km','dryflux5km','dryflux8km','dryflux10km','vaporflux5km','vaporflux8km','vaporflux10km','netcondflux5km','netcondflux8km','netcondflux10km','delzmax','wmax','dryfluxmax','vaporfluxmax','netcondfluxmax','heightdelzmax','heightwmax','heightdryfluxmax','heightvaporfluxmax','heightnetcondfluxmax']

varlist = ['delheight0db','delheight5db','delheight10db','delheight20db','w0db','w5db','w10db','w20db','delzmax','wmax','dryfluxmax','vaporfluxmax','netcondfluxmax']


for time in times:
    for a, var1 in enumerate(varlist):
        for b in range(a,len(varlist)):
            var2 = varlist[b]
            print var1,var2
            vv1 = []
            vv2 = []
            hcheck = []
            for xdir in modeldirs:
                fil = '../h5files/'+time+'/'+time+'-'+xdir+'-2dvars-smoothed3km.h5'
                v1 = getvar(fil,var1)
                v2 = getvar(fil,var2)
                h1 = getvar(fil,'height0db')
                vv1.extend(v1)
                vv2.extend(v2)
                hcheck.extend(v2)
            v1 = np.asarray(vv1)
            v2 = np.asarray(vv2)
            h = np.asarray(hcheck)

            v1 = v1[h>0]
            v2 = v2[h>0]

            plt.hist2d(v1.flatten(),v2.flatten(),bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
            plt.xlabel(var1)
            plt.ylabel(var2)
            plt.savefig(time+'-hist2d-'+var1+'-'+var2+'.png')
            plt.grid('off')
            plt.clf()

        tmp = sorted(v1.flatten())
        





