import numpy as np
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar

def getbudgetvars(fil1,fil2,varname):
    cond = getvar(fil1, varname)*100.*100.*100.
    w = getvar(fil2, 'w')
    massflux = cond*w
    return massflux,w

def upgt5(upflux,w):
    colmax = np.max(w,0)
    w1 = np.where(colmax>5)
    updraft = upflux[:,w1[0],w1[1]]
    up = np.mean(updraft,1)
    warea = len(w1[0])
    return up,warea

def upthresh(upflux, w, height, zval, thresh):
    h = np.argmin(np.abs(height-zval))
    colh = w[h,:,:]
    w1 = np.where(colh>thresh)
    updraft = upflux[:,w1[0],w1[1]]
    up = np.mean(updraft,1)
    warea = len(w1[0])
    return up,warea

modeldirs = pert75()
varnames = ['tracer002','tracer003','tracer004','tracer005','tracer006']
for varname in varnames:
    meanup5 = {}
    meanup81 = {}
    allarea5 = {}
    allarea81 = {}
    for xdir in modeldirs:
        print varname, xdir
        tfiles = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/trac*h5'))
        wfiles = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'*h5'))
        height = getvar(wfiles[0],'z_coords')
        nt = len(tfiles)
        meanup5[xdir] = np.zeros((len(height),nt))
        meanup81[xdir] = np.zeros((len(height),nt))
        allarea5[xdir] = np.zeros(nt)
        allarea81[xdir] = np.zeros(nt)
        for t in range(nt):
            print t
            upflux,w= getbudgetvars(tfiles[t],wfiles[t],varname)
            up5,area5 = upgt5(upflux,w)
            up81,area81 = upthresh(upflux,w,height,8000.,1.)
            meanup5[xdir][:,t] = up5
            allarea5[xdir][t] = area5
            meanup81[xdir][:,t] = up81
            allarea81[xdir][t] = area81

    np.savez(varname+'-updraftflux-wgt5.npz',**meanup5)
    np.savez(varname+'-updraftflux-w8kmgt1.npz',**meanup81)
    np.savez(varname+'-updraftflux-wgt5-updraftarea.npz',**allarea5)
    np.savez(varname+'-updraftflux-w8kmgt1-updraftarea.npz',**allarea81)




