import numpy as np
import h5py as hdf
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from rachelutils.hdfload import getvar
from rachelutils.hdfload import getdz
import matplotlib.animation as animation
from rachelutils.genericplots import movie

#Some constants
cp = 1004.
rd = 287.
kappa = rd/cp
ps = 1000.

def plots(maindir, stage, xdir):
    filesrams = sorted(glob.glob(maindir+stage+'/'+xdir+'/*h5'))
    nt = len(filesrams)
    timemax = np.zeros(nt)
    massadd = np.zeros(nt)
    masscondflux = np.zeros(nt)
    flux500 = []
    w5 = []
    w8 = []
    totmass = np.zeros(nt)
    massdiff = np.zeros(nt)
    microadd = np.zeros(nt)
    pcp3d = np.zeros(nt)
    for tim in range(nt):
        fil = hdf.File(filesrams[tim],'r')
        w = getvar(fil, 'w')
        q = getvar(fil,'total_cond')/1000.
        v = getvar(fil,'vapor')/1000. 
        precip = getvar(fil, 'precip3d')
        rho = (getvar(fil,'press')*100)/(getvar(fil,'tempk')*rd)
        micro = (getvar(fil,'nuccldrt')+getvar(fil,'nucicert')+getvar(fil,'vapicet')+getvar(fil,'vapliqt'))/1000.
        dz = getdz(fil)
        fil.close()
        
        massfluxcond = w*q*rho
        massflux = w*(q+v)*rho
        timemax[tim] = np.max(massfluxcond[39,125:175,200:250])
        flux500.append(massflux[39,125:175,200:250])
        w[w<1]=0
        w5.append(w[39,:,:])
        w8.append(w[46,:,:])
        mass = (q+v)*rho*dz[:,None,None]
        totmic = micro*rho*dz[:,None,None]
        totmass[tim] = np.sum(mass[39:,125:175,200:250])*250*250
        massadd[tim]=np.sum(massflux[39,125:175,200:250])*250*250*30
        masscondflux[tim] = np.sum(massfluxcond[39,125:175,200:250])*250*250*30
        microadd[tim] = np.sum(totmic[39:,125:175,200:250])*250*250
        pcp3d[tim] = np.sum(precip[39,125:175,200:250])*250*250*30*-1

    massdiff[1:]=np.diff(totmass)
    plt.plot(massdiff, linewidth=3)
    plt.title('mass difference (kg)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/massdiff.png')
    plt.clf()
    movie(flux500,'/nobackup/rstorer/plots/massfluxplots/'+xdir+stage,'massflux500mb')
    movie(w5,'/nobackup/rstorer/plots/massfluxplots/'+xdir+stage,'w500mb')
    movie(w8,'/nobackup/rstorer/plots/massfluxplots/'+xdir+stage,'w8km')
    plt.plot(massadd, linewidth=3)
    plt.title('Mass added through vertical flux 500mb (kg)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/massfluxadded.png')
    plt.clf()
    plt.plot(timemax,linewidth=3)
    plt.title('Max Mass Flux at 500mb (kg/m2s)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/timemax.png')
    plt.clf()
    plt.plot(totmass,linewidth=3)
    plt.title('Condensate above 500mb (kg)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/totmass.png')
    plt.clf()
    plt.plot(massadd, linewidth=3, label = 'vertical flux')
    plt.plot(masscondflux, linewidth=3, label = 'cond flux')
#    plt.plot(microadd, linewidth = 3, label = 'micro')
    plt.plot(pcp3d, linewidth=3, label = 'precip')
    plt.plot((pcp3d+massadd), linewidth=3, label = 'sum')
    plt.plot(massdiff, linewidth=3, label = 'diff')
    plt.legend()
    plt.title('Mass Budget above 500mb (kg)')
    plt.savefig('/nobackup/rstorer/plots/massfluxplots/newbudget-growing-125-200.png')
    plt.clf()
maindir = '/nobackup/rstorer/convperts/'
stage = 'mature'
xdir = 'feb23-control'
plots(maindir, stage, xdir)



