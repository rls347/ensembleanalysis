import numpy as np
import h5py as hdf
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar
from rachelutils.hdfload import getdz
import matplotlib.animation as animation
import pickle

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
    
    plt.plot(totflux, linewidth=3, label = 'total updraft flux')
    plt.plot(condflux, linewidth=3, label = 'condensate updraft')
    plt.plot(pcp3d, linewidth=3, label = 'precip')
    plt.plot(netcond, linewidth=3, label = 'net condensate flux')
    plt.plot(netvert, linewidth=3, label = 'net vertical flux')
    plt.plot(massdiff, linewidth=3, label = 'Actual Mass Change')
    plt.legend()
    plt.title('Mass Budget above '+flag+' (kg)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/newbudget-'+xdir+'-'+stage+'-'+location+'-'+flag+'.png')
    plt.clf()

    return [totflux,condflux,pcp3d,netcond,netvert,massdiff]

maindir = '/nobackup/rstorer/convperts/'
lifestages = [('revu',300),('growing',30),('mature',30)]
xdirs = pert75()
#xdirs = ['feb23-control','aug11-control','aug17-control']
locales = [ [125, 175, 200, 250, '50x50'],
            [100, 300, 100, 300, 'mid200'],
            [0, -1, 0, -1, 'domain']] 


allvars = {}
for stage in lifestages:
    stagename = stage[0]
    allvars[stagename]={}
    for xdir in xdirs:
        allvars[stagename][xdir]={}
        for locale in locales:
            locname = locale[4]
            print maindir, stage, xdir, locale
            values = plots(maindir, stage, xdir, locale, '500mb')
            allvars[stagename][xdir][locname]=values

np.savez('massbudget_500mb.npz', **allvars)

secondvars = {}
for stage in lifestages:
    stagename = stage[0]
    secondvars[stagename]={}
    for xdir in xdirs:
        secondvars[stagename][xdir]={}
        for locale in locales:
            locname = locale[4]
            print maindir, stage, xdir, locale
            values = plots(maindir, stage, xdir, locale, '8km')
            secondvars[stagename][xdir][locname]=values

np.savez('massbudget_8km.npz', **secondvars)




