import numpy as np
import h5py as hdf
import glob
from rachelutils.hdfload import getvar, getdz
from rachelutils.dumbnaming import pert75
from rachelutils.genericplots import timeseries
from rachelutils.thermo import satmixratio

def get3levels(filename,varname):
    hfile = hdf.File(filename,'r')
    press = getvar(hfile,'press')
    tempk = getvar(hfile,'tempk')
    rho = (press*100.)/ (287.*tempk)
    vartoavg = getvar(hfile,varname)
    dz = getdz(hfile)
    hfile.close()
                                                        
    vall = vartoavg * rho * dz[:,None,None]
    mass = rho * dz[:,None,None]

    vtop = np.mean(np.mean(vall,1),1)
    vbot = np.mean(np.mean(mass,1),1)
    mpress = np.mean(np.mean(press,1),1)

    lows = np.where(mpress > 850.)
    mids = np.logical_and(mpress < 850, mpress > 500)
    highs = np.where(mpress < 500)

    lowsat = np.sum(vtop[lows]) / np.sum(vbot[lows])
    midsat = np.sum(vtop[mids]) / np.sum(vbot[mids])
    highsat = np.sum(vtop[highs]) / np.sum(vbot[highs])
    allsat = np.sum(vtop) / np.sum(vbot)

    return lowsat, midsat, highsat, allsat


modeldirs = pert75()
modeldirs = ['feb23-control','aug11-control','aug17-control']
for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nfiles = len(files)
    print xdir, nfiles
    xs = np.arange(nfiles)*5

    lowrh = np.zeros(nfiles)
    midrh = np.zeros(nfiles)
    highrh = np.zeros(nfiles)
    allrh = np.zeros(nfiles)

    lowtk = np.zeros(nfiles)
    midtk = np.zeros(nfiles)
    hightk = np.zeros(nfiles)
    alltk = np.zeros(nfiles)

    lowvap = np.zeros(nfiles)
    midvap = np.zeros(nfiles)
    highvap = np.zeros(nfiles)
    allvap = np.zeros(nfiles)

    lowt2 = np.zeros(nfiles)
    midt2 = np.zeros(nfiles)
    hight2 = np.zeros(nfiles)
    allt2 = np.zeros(nfiles)

    for i, filename in enumerate(files):
        lowrh[i],midrh[i],highrh[i],allrh[i] = get3levels(filename,'relhum')
        lowtk[i],midtk[i],hightk[i],alltk[i] = get3levels(filename, 'tempk')
        lowvap[i],midvap[i],highvap[i],allvap[i] = get3levels(filename, 'vapor')
        lowt2[i],midt2[i],hight2[i],allt2[i] = get3levels(filename,'tracer002')

    timeseries(highrh, xs, '/nobackup/rstorer/plots/timeseries-relhumhigh-'+xdir+'.png', 'Upper Level RH (p<500mb)', 'Minutes', 'Percent')
    timeseries(midrh, xs, '/nobackup/rstorer/plots/timeseries-relhummid-'+xdir+'.png', 'Mid Level RH (850mb<p<500mb)', 'Minutes', 'Percent')
    timeseries(lowrh, xs, '/nobackup/rstorer/plots/timeseries-relhumlow-'+xdir+'.png', 'Low Level RH (p>850mb)', 'Minutes', 'Percent')
    timeseries(allrh, xs, '/nobackup/rstorer/plots/timeseries-relhumall-'+xdir+'.png', 'Domain RH', 'Minutes', 'Percent')

    timeseries(hightk, xs, '/nobackup/rstorer/plots/timeseries-tempkhigh-'+xdir+'.png', 'Upper Level Temperature (p<500mb)', 'Minutes', 'K')
    timeseries(midtk, xs, '/nobackup/rstorer/plots/timeseries-tempkmid-'+xdir+'.png', 'Mid Level Temperature (850mb<p<500mb)', 'Minutes', 'K')
    timeseries(lowtk, xs, '/nobackup/rstorer/plots/timeseries-tempklow-'+xdir+'.png', 'Low Level Temperature (p>850mb)', 'Minutes', 'K')
    timeseries(alltk, xs, '/nobackup/rstorer/plots/timeseries-tempkall-'+xdir+'.png', 'Domain Temperature', 'Minutes', 'K')

    timeseries(highvap, xs, '/nobackup/rstorer/plots/timeseries-vaporhigh-'+xdir+'.png', 'Upper Level Vapor (p<500mb)', 'Minutes', 'g/kg')
    timeseries(midvap, xs, '/nobackup/rstorer/plots/timeseries-vapormid-'+xdir+'.png', 'Mid Level Vapor (850mb<p<500mb)', 'Minutes', 'g/kg')
    timeseries(lowvap, xs, '/nobackup/rstorer/plots/timeseries-vaporlow-'+xdir+'.png', 'Low Level Vapor (p>850mb)', 'Minutes', 'g/kg')
    timeseries(allvap, xs, '/nobackup/rstorer/plots/timeseries-vaporall-'+xdir+'.png', 'Domain Vapor', 'Minutes', 'g/kg')

    timeseries(hight2, xs, '/nobackup/rstorer/plots/timeseries-tracer2high-'+xdir+'.png', 'Upper Level Tracer (p<500mb)', 'Minutes', '#/cm3')
    timeseries(midt2, xs, '/nobackup/rstorer/plots/timeseries-tracer2mid-'+xdir+'.png', 'Mid Level Tracer (850mb<p<500mb)', 'Minutes', '#/cm3')
    timeseries(lowt2, xs, '/nobackup/rstorer/plots/timeseries-tracer2low-'+xdir+'.png', 'Low Level Tracer (p>850mb)', 'Minutes', '#/cm3')
    timeseries(allt2, xs, '/nobackup/rstorer/plots/timeseries-tracer2all-'+xdir+'.png', 'Domain Tracer', 'Minutes', '#/cm3')




