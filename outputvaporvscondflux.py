import numpy as np
import h5py as hdf
import glob
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar
from rachelutils.hdfload import getdz

#Some constants
cp = 1004.
rd = 287.
kappa = rd/cp
ps = 1000.

def plots(maindir, stagevar, xdir, locvars, flag):
    if flag == '500mb':
        zval = 39
    if flag == '8km':
        zval = 46
    i1, i2, j1, j2, location = locvars
    stage, dt = stagevar
    filesrams = sorted(glob.glob(maindir+stage+'/'+xdir+'/*h5'))
    nt = len(filesrams)
    totflux= np.zeros(nt)
    condflux= np.zeros(nt)
    totmass = np.zeros(nt)
    massdiff = np.zeros(nt)
    pcp3d = np.zeros(nt)
    for tim in range(nt):
        fil = hdf.File(filesrams[tim],'r')
        w = getvar(fil, 'w')
        q = getvar(fil,'total_cond')/1000.
        v = getvar(fil,'vapor')/1000. 
        precip = getvar(fil, 'precip3d')
        rho = (getvar(fil,'press')*100)/(getvar(fil,'tempk')*rd)
        dz = getdz(fil)
        fil.close()
        
        massfluxcond = w*q*rho
        massfluxtot = w*(q+v)*rho
        masstot = (q+v)*rho*dz[:,None,None]

        totmass[tim] = np.sum(masstot[zval:,i1:i2,j1:j2])*250*250
        totflux[tim]=np.sum(massfluxtot[zval,i1:i2,j1:j2])*250*250*dt
        condflux[tim] = np.sum(massfluxcond[zval,i1:i2,j1:j2])*250*250*dt
        pcp3d[tim] = np.sum(precip[zval,i1:i2,j1:j2])*250*250*dt*-1

    massdiff[1:]=np.diff(totmass)
    netcond = pcp3d + condflux
    netvert = pcp3d + totflux
    
    return [totflux,condflux,pcp3d,netcond,netvert,massdiff]

maindir = '/nobackup/rstorer/convperts/'
lifestages = [('revu',300),('growing',30),('mature',30)]
xdirs = pert75()
#xdirs = ['feb23-control','aug11-control','aug17-control']
locales = [ [125, 175, 200, 250, '50x50'],
            [100, 300, 100, 300, 'mid200'],
            [0, -1, 0, -1, 'domain']] 


#for stage in lifestages:
#    totflux = {}
#    condflux = {}
#    pcp3d = {}
#    netcond = {}
#    netvert = {}
#    massdiff = {}
#    stagename = stage[0]
#    for xdir in xdirs:
#        locale = locales[2]
#        locname = locale[4]
#        print maindir, stage, xdir, locale
#        values = plots(maindir, stage, xdir, locale, '8km')
#        totflux[xdir],condflux[xdir],pcp3d[xdir],netcond[xdir],netvert[xdir],massdiff[xdir]=values
#    outnam = '/nobackup/rstorer/filesnpz/'+stagename+locname
#    np.savez(outnam+'totalwaterflux_8km.npz', **totflux)
#    np.savez(outnam+'condensateflux_8km.npz', **condflux)
#    np.savez(outnam+'pcp3d_8km.npz', **pcp3d)
#    np.savez(outnam+'netcondflux_8km.npz', **netcond)
#    np.savez(outnam+'nettotalwaterflux_8km.npz', **netvert)
#    np.savez(outnam+'totalwatermassdiff_8km.npz', **massdiff)

for stage in lifestages:
    totflux = {}
    condflux = {}
    pcp3d = {}
    netcond = {}
    netvert = {}
    massdiff = {}
    stagename = stage[0]
    for xdir in xdirs:
        locale = locales[2]
        locname = locale[4]
        print maindir, stage, xdir, locale
        values = plots(maindir, stage, xdir, locale, '500mb')
        totflux[xdir],condflux[xdir],pcp3d[xdir],netcond[xdir],netvert[xdir],massdiff[xdir]=values
    outnam = '/nobackup/rstorer/filesnpz/'+stagename+locname
    np.savez(outnam+'totalwaterflux_500mb.npz', **totflux)
    np.savez(outnam+'condensateflux_500mb.npz', **condflux)
    np.savez(outnam+'pcp3d_500mb.npz', **pcp3d)
    np.savez(outnam+'netcondflux_500mb.npz', **netcond)
    np.savez(outnam+'nettotalwaterflux_500mb.npz', **netvert)
    np.savez(outnam+'totalwatermassdiff_500mb.npz', **massdiff)
