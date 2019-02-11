import numpy as np
import h5py as hdf
from rachelutils.hdfload import getvar,getrho
from rachelutils.dumbnaming import pert75
import glob

    
modeldirs = pert75()

times = ['mature','growing']

for xdir in modeldirs:
    rho = getrho('../convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5')[:,0,0]
    for time in times:
        print xdir, time
        wfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*refbudgetvars*h5'))
        vfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*vapor*h5'))
        cfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*cond*h5'))
        pfiles = sorted(glob.glob('../h5files/'+time+'/*'+xdir+'-*precip3d*h5'))
        nt = len(wfiles)
        for t in range(nt):
            print t
            w = getvar(wfiles[t],'w')
            v = getvar(vfiles[t],'q')/1000.
            c = getvar(cfiles[t],'q')/1000.
            p = getvar(pfiles[t],'q')

            dryflux = w*rho[:,None,None]
            vflux = w*rho[:,None,None]*v
            cflux = (w*rho[:,None,None]*c) - p

            tout = str(t)
            if t<10:
                tout = '0'+tout
            outfilename = time+'-'+xdir+'-3dfluxes-smoothed3km-'+tout+'.h5'

            hf = hdf.File(outfilename,'w')
            hf.create_dataset('dryflux',data=dryflux)
            hf.create_dataset('vaporflux',data=vflux)
            hf.create_dataset('netcondflux',data=cflux)
            hf.close()
