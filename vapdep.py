import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar
from rachelutils.dumbnaming import pert75
import numpy as np
import h5py as hdf
import glob


def plotstuff(xs, ys, labelname, xlab, ylab, outname,xpos,ypos):
    xd = xs
    yd = ys
#    fig,ax = plt.subplots(111)
#    plt.scatter(xd, yd, s=30, alpha=0.15, marker='o',color='blue')
    par = np.polyfit(xd, yd, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    xl = [min(xd), max(xd)]
    yl = [slope*xx + intercept  for xx in xl]

    variance = np.var(yd)
    residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
#    ax = plt.gca()
#    plt.text(xpos,ypos,'$R^2 = %0.2f$'% Rsqr +'  slope = $%.4f$'% slope,color ='black',transform = ax.transAxes)
#    plt.plot(xl, yl,linewidth=2,color='black',label=labelname)
#    plt.xlabel(xlab)
#    plt.ylabel(ylab)
#    plt.legend(loc = 'upper center')
#    plt.savefig(outname)
#    plt.clf()
    print slope,'slope'
    return xl,yl,Rsqr,slope

def modelvars(fil,arg):
    graup = (getvar(fil, 'VAPGRAUT')+getvar(fil,'VAPHAILT'))*2*1000.
    ice = (getvar(fil, 'VAPPRIST')+getvar(fil,'VAPSNOWT')+getvar(fil,'VAPAGGRT'))*2*1000.
    rain = (getvar(fil, 'VAPRAINT')+getvar(fil,'VAPDRIZT'))*2*1000.
    cloud = (getvar(fil,'VAPCLDT'))*2*1000.
    temp= (getvar(fil, 'THETA')*getvar(fil,'PI')/1004.)[:,10,10]
    w = getvar(fil, 'WP')
    return graup[arg:,:,:],ice[arg:,:,:],rain[arg:,:,:],cloud[arg:,:,:],w[arg:,:,:],temp[arg:]

alldirs = pert75()
alldirs = ['aug17-control','feb23-control','aug11-control']
height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')
h5km = np.argmin(np.abs(height-5000.))
minarray = np.arange(-80,0,5)+273.15

alphavals = {}
rvals = {}


for xdir in alldirs:
    alphavals[xdir] = np.zeros_like(minarray)
    rvals[xdir]=np.zeros_like(minarray)
    outgraup= []
    outice = []
    outrain = []
    outcloud = []
    outw = []
    for i in range(len(minarray)):
        outgraup.append([])
        outice.append([])
        outrain.append([])
        outcloud.append([])
        outw.append([])
    files = sorted(glob.glob('/nobackup/rstorer/convperts/mature-orig/'+xdir+'/*h5'))
    nt = len(files)    
    for t in range(1,nt):
        print xdir, t
        graup,ice,rain,cloud,w,temp = modelvars(files[t],h5km)
        graup = graup+ice+rain+cloud
        for tval, num in enumerate(minarray):
            tempmin = num
            tempmax = num+5

            cold = np.where(np.logical_and(temp>tempmin,temp<tempmax))

            cgraup = graup[cold,:,:]
#            cice = ice[cold,:,:]
#            crain = rain[cold,:,:]
#            ccloud = cloud[cold,:,:]
            cw = w[cold,:,:]
    
            cg = cgraup[cw>1]
#            ci = cice[cw<-1]
#            cr = crain[cw<-1]
#            cc = ccloud[cw<-1]
            ww = cw[cw<-1]

            outgraup[tval].extend(cg)
#            outrain[tval].extend(cr)
#            outcloud[tval].extend(cc)
#            outice[tval].extend(ci)
            outw[tval].extend(ww)

    for tval,num in enumerate(minarray):
        tempmin = num
        try:
            w = np.asarray(outw[tval])
            graup = np.asarray(outgraup[tval])
#            cloud = np.asarray(outcloud[tval])
#            ice = np.asarray(outice[tval])
#            rain = np.asarray(outrain[tval])
#            allvap = graup+cloud+ice+rain
            allvap = graup

            xl,yl,Rsqr,slope = plotstuff(w, allvap, 'sum', 'w (m/s)', 'Vapor Deposition (g/kg/min)', 'dummy.png',.4,.83)

#            f = np.asarray((graup,ice,rain,cloud))
#            colind = np.argmax(f,0)
#            colors = ['gold','green','blue','purple']
#            lab = ['Graup+Hail','Pris/Snow/Agg','Rain+Driz','Cloud']
#            for c in range(3,-1,-1):
#                xd = w[colind==c]
#                yd = allvap[colind==c]
#                plt.scatter(xd, yd, s=30, alpha=0.15, marker='o',color=colors[c],label = lab[c])

#            ax = plt.gca()
#            plt.text(.4,.83,'$R^2 = %0.2f$'% Rsqr +'  slope = $%.4f$'% slope,color ='black',transform = ax.transAxes)
#            plt.plot(xl, yl,linewidth=2,color='black')
#            plt.xlabel('w (m/s)')
#            plt.ylabel('Vapor Deposition (g/kg/min)')
#            plt.legend(loc = 'upper center')
#            plt.savefig('vapwsplit-'+xdir+'updraft'+str(tempmin)+'.png')
#            plt.clf()

            alphavals[xdir][tval]=slope
            rvals[xdir][tval]=Rsqr
        except:
            print 'no values in ',tempmin
xdir='aug11-control'
plt.plot(minarray,alphavals[xdir],label = [xdir],color='blue',marker='o')
plt.plot(minarray,alphavals[xdir],color='blue',linewidth=2)
xdir='aug17-control'
plt.plot(minarray,alphavals[xdir],label = [xdir],color='orange',marker='o')
plt.plot(minarray,alphavals[xdir],color='orange',linewidth=2)
xdir='feb23-control'
plt.plot(minarray,alphavals[xdir],label = [xdir],color='purple',marker='o')
plt.plot(minarray,alphavals[xdir],color='purple',linewidth=2)
plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Alpha')
plt.savefig('alphacurves-updraft-tot.png')
plt.clf()


xdir='aug11-control'
plt.plot(minarray,rvals[xdir],label = [xdir],color='blue',marker='o')
plt.plot(minarray,rvals[xdir],color='blue',linewidth=2)
xdir='aug17-control'
plt.plot(minarray,rvals[xdir],label = [xdir],color='orange',marker='o')
plt.plot(minarray,rvals[xdir],color='orange',linewidth=2)
xdir='feb23-control'
plt.plot(minarray,rvals[xdir],label = [xdir],color='purple',marker='o')
plt.plot(minarray,rvals[xdir],color='purple',linewidth=2)
plt.legend(loc='upper left')
plt.xlabel('Temperature (K)')
plt.ylabel('Rsqr')
plt.savefig('rcurves-updraft-tot.png')
plt.clf()
