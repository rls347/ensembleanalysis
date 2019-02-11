import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def gettracer(dirname):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dirname+'/*h5'))
    outdir = '/nobackup/rstorer/plots/'
    nt = len(files)
    t2 = getvar(files[0],'tracer002')[:,100,100]
    dz = getdz(files[0])
    x = t2*dz*100*100*100
    return np.sum(x)

def makesum(varin):
    varout = {}
    for nam in varin.keys():
        x = varin[nam]
        x[np.isnan(x)]=0.
        y=np.cumsum(x)
        varout[nam]=y
    return varout

dirs = pert75()
cols = []
for i in range(25):
    cols.append('m')
for i in range(25):
    cols.append('c')
for i in range(25):
    cols.append('y')


initval = {}
for i, dirname in enumerate(dirs):
    initval[dirname]=gettracer(dirname)
sallupdraft = np.load('../filesnpz/budget-timeseries-updrafttracer2flux.npz')
allupdraft = makesum(sallupdraft)
#allupdraft = np.load('../filesnpz/budget-total-updrafttracer2flux.npz')
height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')
precipvals= np.load('../filesnpz/totpcpmm.npz')


varlist = ['rhhigh','rhmid','rhlow','init_vertintvap','cape_ML','shear','ltss']
varlist = ['rhlow']
for varname in varlist:
    fil = '../filesnpz/'+varname+'.npz'
    allrh = np.load(fil)
    rh = np.zeros(75)
    pcp = np.zeros(75)
    init_trac = np.zeros(75)
    up = np.zeros(75)
    updiv = np.zeros(75)
    upinit = np.zeros(75)
    updivinit = np.zeros(75)
    for i,xdir in enumerate(dirs):
        rh[i]=allrh[xdir]
        init_trac[i] = initval[xdir]
        pcp[i]=precipvals[xdir]/(400.*400.)
        up[i]=allupdraft[xdir][-1]
        upinit[i] = allupdraft[xdir][-1]/initval[xdir]
        updiv[i]=up[i]/pcp[i]
        updivinit[i] = upinit[i]/pcp[i]

    plt.scatter(rh,upinit,color=cols)
    p = np.poly1d(np.polyfit(rh,upinit,2))
    variance = np.var(upinit)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,upinit)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(rh.min(),rh.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Tracer Flux')
    ax.set_xlabel(varname)
    ax.set_title('Integrated Tracer Flux at 8 km')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(rh,upinit,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(rh,upinit)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('tracervs'+varname+'scatterfit-scaledbyinit.png')
    plt.clf()


    plt.scatter(rh,updivinit,color=cols)
    p = np.poly1d(np.polyfit(rh,updivinit,2))
    variance = np.var(updivinit)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,updivinit)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(rh.min(),rh.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Tracer Flux/Precip')
    ax.set_xlabel(varname)
    ax.set_title('Integrated Tracer Flux at 8 km/total precip')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(rh,updivinit,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(rh,updivinit)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('tracerdivprecipvs'+varname+'scatterfit-scaledbyinit.png')
    plt.clf()

    plt.scatter(rh,up,color=cols)
    p = np.poly1d(np.polyfit(rh,up,2))
    variance = np.var(up)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,up)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(rh.min(),rh.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Tracer Flux')
    ax.set_xlabel(varname)
    ax.set_title('Integrated Tracer Flux at 8 km')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(rh,up,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(rh,up)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('tracervs'+varname+'scatterfit.png')
    plt.clf()


    plt.scatter(rh,updiv,color=cols)
    p = np.poly1d(np.polyfit(rh,updiv,2))
    variance = np.var(updiv)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,updiv)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(rh.min(),rh.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Tracer Flux/Precip')
    ax.set_xlabel(varname)
    ax.set_title('Integrated Tracer Flux at 8 km/total precip')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(rh,updiv,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(rh,updiv)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('tracerdivprecipvs'+varname+'scatterfit.png')
    plt.clf()


    plt.scatter(pcp,upinit,color=cols)
    p = np.poly1d(np.polyfit(pcp,upinit,2))
    variance = np.var(upinit)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(pcp,upinit)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(pcp.min(),pcp.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Tracer Flux')
    ax.set_xlabel('Precip')
    ax.set_title('Integrated Tracer Flux at 8 km vs Total Precip')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(pcp,upinit,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(pcp,upinit)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('precipvstracerflux-scatterfit-scaledbyinit.png')
    plt.clf()


    plt.scatter(rh,pcp,color=cols)
    p = np.poly1d(np.polyfit(rh,pcp,2))
    variance = np.var(pcp)
    residuals = np.var([(p(xx)-yy) for xx, yy in zip(rh,pcp)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    xp = np.linspace(rh.min(),rh.max(),100)
    plt.plot(xp,p(xp),color='black')
    ax = plt.gca()
    ax.set_ylabel('Precip')
    ax.set_xlabel(varname)
    ax.set_title('Total Precip')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    p2 = np.poly1d(np.polyfit(rh,pcp,1))
    resid = np.var([(p2(xx)-yy) for xx, yy in zip(rh,pcp)])
    rsq2 = np.round(1-resid/variance,decimals=2)
    plt.plot(xp,p2(xp),color='green')
    plt.text(.2,.65,'$R^2 = %0.2f$'% rsq2 ,color ='green',transform = ax.transAxes)
    plt.savefig('precipvs'+varname+'scatterfit.png')
    plt.clf()




