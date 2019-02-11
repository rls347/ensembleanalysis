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

    columnvapor = np.sum(vact[layer])/1000.
    columnrh = 100. * (np.sum(vact[layer]) / np.sum(vsat[layer]))
    print columnvapor, columnrh

    return columnvapor, columnrh

def getrhbyz(fil,bottom,top):
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

    layer = np.logical_and(heights > bottom, heights< top)

    columnvapor = np.sum(vact[layer])
    columnrh = 100. * (np.sum(vact[layer]) / np.sum(vsat[layer]))

    return columnvapor, columnrh


def getlayer(modeldirs,bot,top,lab):
    vapout = {}
    rhout = {}

    for xdir in modeldirs:
        files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
        if lab == 'press':
            colvap,colsat = getrh(files[0],bot,top)
        else:
            colvap,colsat = getrhbyz(files[0],bot,top)
        vapout[xdir] = colvap
        rhout[xdir] = colsat
    np.savez('rh-'+lab+'-'+str(bot)+'-'+str(top)+'.npz',**rhout)
    np.savez('colvap-'+lab+'-'+str(bot)+'-'+str(top)+'.npz',**vapout)


modeldirs = pert75()
getlayer(modeldirs,1000,900,'press')
getlayer(modeldirs,900,800,'press')
getlayer(modeldirs,800,700,'press')
getlayer(modeldirs,700,600,'press')
getlayer(modeldirs,600,500,'press')
getlayer(modeldirs,500,100,'press')
getlayer(modeldirs,950,750,'press')
getlayer(modeldirs,750,400,'press')
getlayer(modeldirs,1000,850,'press')
getlayer(modeldirs,850,500,'press')

getlayer(modeldirs,0,2000,'z')
getlayer(modeldirs,2000,4000,'z')
getlayer(modeldirs,4000,6000,'z')
getlayer(modeldirs,6000,8000,'z')
getlayer(modeldirs,8000,10000,'z')


getlayer(modeldirs,0,20000,'z')
getlayer(modeldirs,1000,100,'press')

getlayer(modeldirs,1000,10,'press')




