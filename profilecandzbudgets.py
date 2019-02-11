import numpy as np
import matplotlib
matplotlib.use("Agg")
from rachelutils.hdfload import getvar
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
    nt = len(budfiles)
    profsc = []
    profsz = []
    profln = []
    for i in range(nt):
        delz = getvar(budfiles[i],'ref2') - getvar(budfiles[i],'ref')
        onec = getvar(condfiles[i],'q')
        delc = (getvar(condfiles[i+3],'q') - getvar(condfiles[i],'q'))
        dlnc = delc/onec
        dlnc[np.isnan(dlnc)]=0.
        dlnc[onec<0.00001]=0.
        w = getvar(budfiles[i],'w')
        maxw = np.max(w,0)
        conv = np.where(maxw>1)
        pz = delz[:,conv[0],conv[1]]
        pc = delc[:,conv[0],conv[1]]
        pl = dlnc[:,conv[0],conv[1]]
        profln.append(pl)
        profsc.append(pc)
        profsz.append(pz)

    scout = np.concatenate(profsc[:],axis=1)
    lnout = np.concatenate(profln[:],axis=1)
    szout = np.concatenate(profsz[:],axis=1)
    
    return scout, szout, lnout


height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')

modeldirs = pert75()

profsc = []
profsz = []
profln = []
for xdir in modeldirs:
    pc,pz,pl = getprofs(xdir)
    profln.append(pl)
    profsc.append(pc)
    profsz.append(pz)

alldelc = np.concatenate(profsc[:],axis=1)
alldelz = np.concatenate(profsz[:],axis=1)
alldlnc = np.concatenate(profln[:],axis=1)
nump = alldelc.shape[1]

for x in range(nump):
    plt.plot(alldelc[:,x],height,color='gray')
mp = np.mean(alldelc,1)
plt.plot(mp,height,color = 'red', linewidth=2)
plt.savefig('delcprofs-1ms.png')
plt.clf()

for x in range(nump):
    plt.plot(alldlnc[:,x],height,color='gray')
mp = np.mean(alldlnc,1)
plt.plot(mp,height,color='red',linewidth=2)
plt.savefig('delclnprofs-1ms.png')
plt.clf()

for x in range(nump):
    plt.plot(alldelz[:,x],height,color='gray')
mp = np.mean(alldelz,1)
plt.plot(mp,height,color = 'red', linewidth=2)
plt.savefig('delzprofs-1ms.png')
plt.clf()


plt.plot(np.mean(alldelc,1)*10,height,color='blue',label='$\Delta$ C',linewidth=3)
plt.plot(np.mean(alldelz,1),height,color='red',label = '$\Delta$ Z',linewidth=3)
plt.plot(np.mean(alldlnc,1),height,color='green',label = '$\Delta$ C / C',linewidth=3)
plt.legend()
plt.savefig('delall-1ms.png')
plt.clf()

height=height/1000.

slopes = np.zeros_like(height)
rsquares = np.zeros_like(height)

for z in range(1,69):
    xs = alldelz[z,:]
    ys = alldelc[z,:]
    rsquares[z],slopes[z] = plotstuff(xs, ys, 'delcdelzscatter-'+str(height[z])+'.png')

plt.plot(slopes,height)
plt.title('slopes')
plt.savefig('delcdelzslopes.png')
plt.clf

plt.plot(rsquares,height)
plt.title('rsquares')
plt.savefig('delcdelzrsquares.png')
plt.clf



slopes = np.zeros_like(height)
rsquares = np.zeros_like(height)

for z in range(1,69):
    xs = alldelz[z,:]
    ys = alldlnc[z,:]
    rsquares[z],slopes[z] = plotstuff(xs, ys, 'delzdlncscatter-'+str(height[z])+'.png')

plt.plot(slopes,height)
plt.title('slopes')
plt.savefig('delzdlncslopes.png')
plt.clf

plt.plot(rsquares,height)
plt.title('rsquares')
plt.savefig('delzdlncrsquares.png')
plt.clf


