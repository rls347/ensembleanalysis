import numpy as np
import h5py as hdf
import glob
from rachelutils.hdfload import getvar, getdz
from rachelutils.dumbnaming import pert75
from rachelutils.genericplots import timeseries
from rachelutils.thermo import satmixratio

def getrh(filename):
    hfile = hdf.File(filename,'r')
    press = getvar(hfile,'press')
    tempk = getvar(hfile,'tempk')
    relhum = getvar(hfile,'relhum')
    rho = (press*100.)/ (287.*tempk)
    vapor = getvar(hfile,'vapor')
    sat = satmixratio(tempk,press)*1000.
    dz = getdz(hfile)
    hfile.close()
                                                        
    vsatall = sat * rho * dz[:,None,None]
    vactall = vapor * rho * dz[:,None,None]

    vsat = np.mean(np.mean(vsatall,1),1)
    vact = np.mean(np.mean(vactall,1),1)
    mpress = np.mean(np.mean(press,1),1)

    lows = np.where(mpress > 850.)
    mids = np.logical_and(mpress < 850, mpress > 500)
    highs = np.where(mpress < 500)

    lowsat = 100. * (np.sum(vact[lows]) / np.sum(vsat[lows]))
    midsat = 100. * (np.sum(vact[mids]) / np.sum(vsat[mids]))
    highsat = 100. * (np.sum(vact[highs]) / np.sum(vsat[highs]))

    return lowsat, midsat, highsat


modeldirs = pert75()
for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nfiles = len(files)
    print xdir, nfiles
    xs = np.arange(nfiles)*5
    lowrh = np.zeros(nfiles)
    midrh = np.zeros(nfiles)
    highrh = np.zeros(nfiles)
    for i, filename in enumerate(files):
        lowrh[i],midrh[i],highrh[i] = getrh(filename)

    timeseries(highrh, xs, '/nobackup/rstorer/plots/timeseries-RHhigh-'+xdir+'.png', 'Upper Level RH (p<500mb)', 'Minutes', 'Percent')
    timeseries(midrh, xs, '/nobackup/rstorer/plots/timeseries-RHmid-'+xdir+'.png', 'Mid Level RH (850mb<p<500mb)', 'Minutes', 'Percent')
    timeseries(lowrh, xs, '/nobackup/rstorer/plots/timeseries-RHlow-'+xdir+'.png', 'Low Level RH (p>850mb)', 'Minutes', 'Percent')



