import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

dirs = pert75()
#dirs = ['aug11-control','feb23-control','aug17-control']

height = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5','z_coords')
dz = getdz('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-001.h5')
zarg = []
for outheight in range(2,13,2):
    zarg.append(np.argmin(np.abs(height-(outheight*1000))))

for zval in zarg:
    times = ['mature','growing']
    for time in times:
        outdzdt = {}
        outdzdx = {}
        outdzdy = {}
        outdzdz = {}
        outw = {}
        outu = {}
        outv = {}
        for xdir in dirs:
            print xdir
            modelfiles = sorted(glob.glob('/nobackup/rstorer/code/budgetfiles/'+time+'*'+xdir+'*h5'))
            nt = len(modelfiles)
            outdzdt[xdir]=[]
            outdzdx[xdir]=[]
            outdzdy[xdir]=[]
            outdzdz[xdir]=[]
            outw[xdir]=[]
            outu[xdir]=[]
            outv[xdir]=[]
            for t in range(nt-3):
                print t
                w = getvar(modelfiles[t],'w')
                u = getvar(modelfiles[t],'u')
                v = getvar(modelfiles[t],'v')
                ref = getvar(modelfiles[t],'ref')
                ref2 = getvar(modelfiles[t],'ref2')

                locs = np.where(np.logical_and((ref>0),(w>1)))
                if len(locs[0]) > 2:
                    for loc in range(len(locs[0])):
                        k,i,j=locs[0][loc],locs[1][loc],locs[2][loc]
                        if k ==zval and i!=0 and i!=32 and j!=0 and j!=32:
                            outdzdt[xdir].append((ref2[k,i,j]-ref[k,i,j])/90.)
                            uu = u[k,i,j]
                            vv = v[k,i,j]
                            if uu>0:
                                outdzdx[xdir].append((ref[k,i,j+1]-ref[k,i,j-1])/6000.)
                            else:
                                outdzdx[xdir].append((ref[k,i,j-1]-ref[k,i,j+1])/6000.)
                            if vv>0:
                                outdzdy[xdir].append((ref[k,i+1,j]-ref[k,i-1,j])/6000.)
                            else:
                                outdzdy[xdir].append((ref[k,i-1,j]-ref[k,i+1,j])/6000.)
                            outdzdz[xdir].append((ref[k+1,i,j]-ref[k-1,i,j])/(dz[k+1]+dz[k]))
                            outu[xdir].append(uu)
                            outv[xdir].append(vv)
                            outw[xdir].append(w[k,i,j])
            outdzdt[xdir]=np.asarray(outdzdt[xdir])
            outdzdx[xdir]=np.asarray(outdzdx[xdir])
            outdzdy[xdir]=np.asarray(outdzdy[xdir])
            outdzdz[xdir]=np.asarray(outdzdz[xdir])
            outw[xdir]=np.asarray(outw[xdir])
            outu[xdir]=np.asarray(outu[xdir])
            outv[xdir]=np.asarray(outv[xdir])
            print len(outv[xdir])

        np.savez(time+'zbudget-dzdt-'+str(zval*1000)+'.npz',**outdzdt)
        np.savez(time+'zbudget-dzdx-'+str(zval*1000)+'.npz',**outdzdx)
        np.savez(time+'zbudget-dzdy-'+str(zval*1000)+'.npz',**outdzdy)
        np.savez(time+'zbudget-dzdz-'+str(zval*1000)+'.npz',**outdzdz)
        np.savez(time+'zbudget-u-'+str(zval*1000)+'.npz',**outu)
        np.savez(time+'zbudget-v-'+str(zval*1000)+'.npz',**outv)
        np.savez(time+'zbudget-w-'+str(zval*1000)+'.npz',**outw)
