import numpy as np
import matplotlib
matplotlib.use("Agg")
from rachelutils.hdfload import getvar,getvar
from rachelutils.dumbnaming import pert75
import glob
import matplotlib.pyplot as plt

def plotstuff(xs, ys, filename):
    plt.scatter(xs,ys)
    par = np.polyfit(xs,ys, 1, full=True)
    slope=par[0][0]
    intercept=par[0][1]
    xl = [min(xs), max(xs)]
    yl = [slope*xx + intercept  for xx in xs]
    variance = np.var(ys)
    residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xs,ys)])
    Rsqr = np.round(1-residuals/variance, decimals=2)

    xp = np.linspace(xs.min(),xs.max(),100)
    plt.plot(xp,(slope*xp+intercept))
    ax = plt.gca()
    ax.set_ylabel('$\Delta$ C')
    ax.set_xlabel('$\Delta$ Z')
#    ax.set_title('Integrated Tracer Flux at 8 km')
    plt.text(.2,.75,'$R^2 = %0.2f$'% Rsqr ,color ='black',transform = ax.transAxes)
    plt.savefig(filename)
    plt.clf()

    return Rsqr,slope

def getprofs(xdir):
    print xdir
    budfiles = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'-refbudgetvars-90s-smoothed*'))
    condfiles = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'-condensate-smoo*'))
    rhofiles = sorted(glob.glob('/nobackup/rstorer/h5files/mature-'+xdir+'-rho-smoo*'))
    nt = len(budfiles)
    profsc = []
    profsz = []
    profln = []
    profactz = []
    profactc = []
    for i in range(nt):
        delz = getvar(budfiles[i],'ref2') - getvar(budfiles[i],'ref')
        onec = 10*np.log10(getvar(condfiles[i],'q')*getvar(rhofiles[i],'q'))
        onec[np.isnan(onec)]=-40 
        onec[onec<-40]=-40.
        onez = getvar(budfiles[i],'ref')
        delc = (10*np.log10(getvar(condfiles[i+3],'q')*getvar(rhofiles[i+3],'q')) - 10*np.log10(getvar(condfiles[i],'q')*getvar(rhofiles[i],'q')))
        delc[delc>40]=40.
        #dlnc = delc/onec
        #dlnc[np.isnan(dlnc)]=0.
        #dlnc[onec<0.00001]=0.
        delc[np.isnan(delc)]=0.
        dlnc = delc
        w = getvar(budfiles[i],'w')
        maxw = np.max(w,0)
        conv = np.where(w>1)
        pz = delz[conv[0],conv[1],conv[2]]
        pc = delc[conv[0],conv[1],conv[2]]
        pl = dlnc[conv[0],conv[1],conv[2]]
        pac = onec[conv[0],conv[1],conv[2]]
        paz = onez[conv[0],conv[1],conv[2]]
        profactz.extend(paz)
        profactc.extend(pac)
        profln.extend(pl)
        profsc.extend(pc)
        profsz.extend(pz)

    scout = np.asarray(profsc)
    lnout = np.asarray(profln[:])
    szout = np.asarray(profsz[:])
    azout = np.asarray(profactz[:])
    acout = np.asarray(profactc[:])
    print scout.min(), lnout.min(), szout.min(), azout.min(), acout.min()
    
    return scout, szout, lnout, azout, acout


height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')

modeldirs = pert75()
modeldirs = ['feb23-control']
profsc = []
profsz = []
profln = []
profactz = []
profactc = []
for xdir in modeldirs:
    pc,pz,pl,az,ac = getprofs(xdir)
    profln.extend(pl)
    profsc.extend(pc)
    profsz.extend(pz)
    profactz.extend(az)
    profactc.extend(ac)

alldelc = np.asarray(profsc[:])
alldelz = np.asarray(profsz[:])
alldlnc = np.asarray(profln[:])
allactz = np.asarray(profactz[:])
allactc = np.asarray(profactc[:])

rsquares,slopes = plotstuff(alldelz, alldelc, 'scatterdelcdelz.png')
plt.hist2d(alldelc,alldelz,bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
plt.xlabel('$\Delta$ Z')
plt.ylabel('$\Delta$ C')
plt.savefig('heatmapdelcdelz.png')
plt.clf()
print rsquares, slopes, 'delta c'

rsquares,slopes = plotstuff(alldelz, alldlnc, 'scatterdlncdelz.png')
print rsquares, slopes, 'd ln c'
plt.hist2d(alldelz,alldlnc,bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
plt.ylabel('$\Delta$ C / C')
plt.xlabel('$\Delta$ Z')
plt.savefig('heatmapdlncdelz.png')
plt.clf()       

rsquares,slopes = plotstuff(allactz, allactc, 'scattercz.png')
print rsquares, slopes, 'c vs z'
plt.hist2d(allactz,allactc,bins = (100,100),cmap=matplotlib.cm.jet, norm=matplotlib.colors.LogNorm())
plt.ylabel('C')
plt.xlabel('Z')
plt.savefig('heatmapcz.png')
plt.clf()







