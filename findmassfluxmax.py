import numpy as np
import glob
import h5py as hdf
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
from rachelutils.genericplots import timeseries

def profilemax(var):
    prof = np.mean(np.mean(var,1),1)
    return np.argmax(prof)

def onevaluemax(b):
    val = np.unravel_index(b.argmax(), b.shape)
    return val[0]

modeldirs = ['feb23-control','aug11-control','aug17-control']

for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nfiles = len(files)
    print xdir, nfiles
    profmaxv = np.zeros(nfiles)
    maxmaxv = np.zeros(nfiles)
    profmaxc = np.zeros(nfiles)
    profmaxt = np.zeros(nfiles)
    maxmaxc = np.zeros(nfiles)
    maxmaxt = np.zeros(nfiles)
    profmaxw = np.zeros(nfiles)
    maxmaxw = np.zeros(nfiles)
    xs = np.arange(nfiles)*5

    for n, filename in enumerate(files):
        fil = hdf.File(filename, 'r')
        height = getvar(fil,'z_coords')
        press = getvar(fil,'press')
        tempk = getvar(fil,'tempk')
        w = getvar(fil,'w')
        rho = (press*100.)/ (287.*tempk) 
        vapor = getvar(fil,'vapor')/1000.
        cond = getvar(fil,'total_cond')/1000.
        tracer = getvar(fil,'tracer002')*(100.**3)

        fluxvap = vapor*rho*w
        fluxcond = cond*rho*w
        fluxtrac = tracer*w

        profmaxv[n] = height[profilemax(fluxvap)]
        profmaxc[n] = height[profilemax(fluxcond)]
        profmaxt[n] = height[profilemax(fluxtrac)]

        maxmaxv[n] = height[onevaluemax(fluxvap)]
        maxmaxc[n] = height[onevaluemax(fluxcond)]
        maxmaxt[n] = height[onevaluemax(fluxtrac)]

        profmaxw[n] = height[profilemax(w)]
        maxmaxw[n] = height[onevaluemax(w)]

    timeseries(profmaxv, xs, '/nobackup/rstorer/plots/timeseries-profmaxheight-vaporflux-'+xdir+'.png', 'Height of Max Vapor Flux (avg prof)', 'Minutes', 'm')
    timeseries(profmaxc, xs, '/nobackup/rstorer/plots/timeseries-profmaxheight-condflux-'+xdir+'.png', 'Height of Max Condensate Flux (avg prof)', 'Minutes', 'm')
    timeseries(profmaxt, xs, '/nobackup/rstorer/plots/timeseries-profmaxheight-tracer2flux-'+xdir+'.png', 'Height of Max Tracer Flux (avg prof)', 'Minutes', 'm')
    timeseries(profmaxw, xs, '/nobackup/rstorer/plots/timeseries-profmaxheight-w-'+xdir+'.png', 'Height of Max Updraft (avg prof)', 'Minutes', 'm')

    timeseries(maxmaxv, xs, '/nobackup/rstorer/plots/timeseries-maxmaxheight-vaporflux-'+xdir+'.png', 'Height of Max Vapor Flux (single value)', 'Minutes', 'm')
    timeseries(maxmaxc, xs, '/nobackup/rstorer/plots/timeseries-maxmaxheight-condflux-'+xdir+'.png', 'Height of Max Condensate Flux (single value)', 'Minutes', 'm')
    timeseries(maxmaxt, xs, '/nobackup/rstorer/plots/timeseries-maxmaxheight-tracer2flux-'+xdir+'.png', 'Height of Max Tracer Flux (single value)', 'Minutes', 'm')
    timeseries(maxmaxw, xs, '/nobackup/rstorer/plots/timeseries-maxmaxheight-w-'+xdir+'.png', 'Height of Max Updraft (single value)', 'Minutes', 'm')


