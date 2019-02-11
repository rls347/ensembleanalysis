import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def getrh(fil,bottom,top):
    heights = getvar(fil,'z_coords')[1:]
    tempk = np.mean(np.mean(getvar(fil,'tempk')[1:,:,:],1),1)
    press = np.mean(np.mean(getvar(fil,'press')[1:,:,:],1),1)
    vapor = np.mean(np.mean(getvar(fil,'vapor')[1:,:,:],1),1)
    rho = (press*100.)/ (287.*tempk)
    dz = getdz(fil)[:-1]

    es = 611.2*np.exp(17.67*(tempk-273.15)/(tempk-29.65))
    rvs = 622*es/((press*100.)-es)

    vsat = rvs * rho * dz
    vact = vapor * rho * dz

    layer = np.logical_and(press < bottom, press > top)

    columnvapor = np.sum(vact[layer])
    columnrh = 100. * (np.sum(vact[layer]) / np.sum(vsat[layer]))

    return columnvapor, columnrh

def timeseriesplot(modeldirs,bot,top):
    rhall = np.load('../filesnpz/rhlow.npz')

    rh = np.zeros(75)
    for i in range(75):
        rh[i] = rhall[modeldirs[i]]

    allvap = []
    allrh = []


    for xdir in modeldirs:
        print xdir
        files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
        nf = len(files)
        colvap = np.zeros(nf)
        colsat = np.zeros(nf)
        for i, f in enumerate(files):
            colvap[i],colsat[i] = getrh(f,bot,top)
        xs = np.arange(nf)*5
        allvap.append((xs,colvap))
        allrh.append((xs,colsat))


    line2 = [zip(x,y) for x, y in allvap]
    fig, ax = plt.subplots()
    lines2 = LineCollection(line2, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines2)
    fig.colorbar(lines2)
    ax.autoscale()
    plt.savefig('timeseries-columnvapor-'+str(bot)+'-'+str(top)+'.png')
    plt.clf()

    line1 = [zip(x,y) for x, y in allrh]
    fig, ax = plt.subplots()
    lines1 = LineCollection(line1, array = rh, cmap = plt.cm.rainbow, linewidth=3)
    ax.add_collection(lines1)
    fig.colorbar(lines1)
    ax.autoscale()
    plt.savefig('timeseries-columnrh-'+str(bot)+'-'+str(top)+'.png')
    plt.clf()



modeldirs = pert75()
timeseriesplot(modeldirs,1000,900)
timeseriesplot(modeldirs,900,800)
timeseriesplot(modeldirs,800,700)
timeseriesplot(modeldirs,700,600)
timeseriesplot(modeldirs,600,500)
timeseriesplot(modeldirs,500,100)
timeseriesplot(modeldirs,950,750)
timeseriesplot(modeldirs,750,400)







