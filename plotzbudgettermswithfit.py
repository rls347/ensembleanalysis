import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.colors import LogNorm
from rachelutils.dumbnaming import pert75,case25


def plotstuff(xs, ys, colors, labelname, xlab, ylab, outname,xpos,ypos):
    #for li in range(len(xs)):
    xd = xs#[li]
    yd = ys#[li]
    #fig,ax = plt.subplots(111)
    plt.scatter(xd, yd, s=30, alpha=0.15, marker='o',color='blue')
    par = np.polyfit(xd, yd, 1, full=True)
    
    slope=par[0][0]
    intercept=par[0][1]
    xl = [min(xd), max(xd)]
    yl = [slope*xx + intercept  for xx in xl]

    variance = np.var(yd)
    residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    ax = plt.gca()
    plt.text(.75,.75,'$R^2 = %0.2f$'% Rsqr +'  slope = $%.4f$'% slope,color = 'black',transform = ax.transAxes)
    plt.plot(xl, yl,linewidth=2,color='black')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend(loc = 'upper center')
    plt.savefig(outname)
    plt.clf()

def getallvars(time,namenum):
    outdzdt = np.load(time+'zbudget-dzdt-control.npz')
    outdzdx = np.load(time+'zbudget-dzdx-control.npz')
    outdzdy = np.load(time+'zbudget-dzdy-control.npz')
    outdzdz = np.load(time+'zbudget-dzdz-control.npz')
    outu = np.load(time+'zbudget-u-control.npz')
    outv = np.load(time+'zbudget-v-control.npz')
    outw = np.load(time+'zbudget-w-control.npz')

    allyterm = []
    allxterm = []
    allzterm = []
    alltterm = []
    allw = []
    allu = []
    allv = []

    for xdir in dirs:
        w = outw[xdir]
        u = outu[xdir]
        v = outv[xdir]
        dzdt = outdzdt[xdir]
        dzdx = outdzdx[xdir]
        dzdy = outdzdy[xdir]
        dzdz = outdzdz[xdir]

        dzdz = dzdz[dzdt>0]
        dzdy = dzdy[dzdt>0]
        dzdx = dzdx[dzdt>0]
        u = u[dzdt>0]
        v = v[dzdt>0]
        w = w[dzdt>0]
        dzdt = dzdt[dzdt>0]

        allw.extend(w)
        allu.extend(u)
        allv.extend(v)
        allxterm.extend(dzdx)
        allyterm.extend(dzdy)
        allzterm.extend(dzdz)
        alltterm.extend(dzdt)

    allyterm = np.asarray(allyterm)
    allxterm = np.asarray(allxterm)
    allzterm = np.asarray(allzterm)
    alltterm = np.asarray(alltterm)
    allw = np.asarray(allw)
    allu = np.asarray(allu)
    allv = np.asarray(allv)
        
    return allu,allv,allw,alltterm,allxterm,allyterm,allzterm


dirs = pert75()
dirs = ['aug17-control','feb23-control','aug11-control']

times = ['growing','mature']
times = ['mature5km','mature8km','mature10km']
namenums = ['40000','46000','50000','54000']
labelname = ['6km','8km','10km','12km']
colors = ['blue','red','green','purple']
xpos=[.75,.75,.75,.75]
ypos = [.2,.4,.6,.8]
for time in times:
    u = [] 
    v = []
    w = []
    dzdt = []
    dzdx = []
    dzdy = []
    dzdz = []

    uvar,vvar,wvar,dzdtvar,dzdxvar,dzdyvar,dzdzvar = getallvars(time,namenums[0])
    u.extend(uvar)
    v.extend(vvar)
    w.extend(wvar)
    dzdt.extend(dzdtvar)
    dzdy.extend(dzdyvar)
    dzdx.extend(dzdxvar)
    dzdz.extend(dzdzvar)


    u =np.asarray(u)
    v = np.asarray(v)
    w = np.asarray(w)
    dzdt = np.asarray(dzdt)
    dzdy = np.asarray(dzdy)
    dzdz = np.asarray(dzdz)
    dzdx = np.asarray(dzdx)

    plotstuff(w, dzdt, colors, labelname, 'w (m/s)', 'dZ/dt', time+'-fitplot-w-dzdt-modelres.png',xpos,ypos)
    plotstuff(w, dzdz, colors, labelname, 'w (m/s)', 'dZ/dz', time+'-fitplot-w-dzdz-modelres.png',xpos,ypos)

    heightterm = w*dzdz
    timeplusheightterm = dzdt+heightterm
    c = u*dzdx + v*dzdy + w*dzdz +dzdt
    lotsofterms = u*dzdx + v*dzdy + dzdt

    plotstuff(w, heightterm, colors, labelname, 'w (m/s)', 'w dZ/dz', time+'-fitplot-w-wdzdz-modelres.png',xpos,ypos)
    plotstuff(w, timeplusheightterm, colors, labelname, 'w (m/s)', 'dZ/dt + w dZ/dz', time+'-fitplot-w-dzdtwdzdz-modelres.png',xpos,ypos)
    plotstuff(w, lotsofterms, colors, labelname, 'w (m/s)', 'dZ/dt + u dZ/dx + v dZ/dy', time+'-fitplot-w-dzdtuv-modelres.png',xpos,ypos)
    plotstuff(w, c, colors, labelname, 'w (m/s)', 'C', time+'-fitplot-w-c-modelres.png',xpos,ypos)

