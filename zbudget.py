import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from rachelutils.dumbnaming import pert75

def smoothedvar(var):
#    smoothvar = np.zeros((45,33,33))-40
    smoothvar = np.zeros((82,33,33))-40
    var[var<-40] = -40
    for h in range(82):
        hind = h#+37
        for i in range(6,402,12):
            iind = (i-6)/12
            for j in range(6,402,12):
                jind = (j-6)/12
                smoothvar[h,iind,jind] = np.mean(var[hind,i-6:i+6,j-6:j+6])
    return smoothvar

dirs = pert75()
#dirs = ['aug11-control','feb23-control','aug17-control']

times = ['mature','growing']
#times = ['mature']
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
        modelfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/'+xdir+'/*h5'))
        radarfiles = sorted(glob.glob('/nobackup/rstorer/convperts/'+time+'/quickbeam/'+xdir+'*h5'))
        height = getvar(modelfiles[0],'z_coords')[37:]
        dz = getdz(modelfiles[0])[37:]
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
            w = smoothedvar(getvar(modelfiles[t],'w'))
            u = smoothedvar(getvar(modelfiles[t],'u'))
            v = smoothedvar(getvar(modelfiles[t],'v'))
            ref = smoothedvar(getvar(radarfiles[t],'reflectivity'))
            ref2 = smoothedvar(getvar(radarfiles[t+3],'reflectivity'))
            tout = str(t)
            if t<10:
                tout = '0'+tout

            outfilename = time+'-'+xdir+'-refbudgetvars-90s-smoothed3km-'+tout+'.h5'
            hf = hdf.File(outfilename,'w')
            hf.create_dataset('u',data=u)
            hf.create_dataset('v',data=v)
            hf.create_dataset('w',data=w)
            hf.create_dataset('ref',data=ref)
            hf.create_dataset('ref2',data=ref2)
            hf.close()

#            locs = np.where(np.logical_and((ref>0),(w>1)))
#            if len(locs[0]) > 2:
#                for loc in range(len(locs[0])):
#                    k,i,j=locs[0][loc],locs[1][loc],locs[2][loc]
#                    if k !=0 and k!=44 and i!=0 and i!=32 and j!=0 and j!=32:
#                        outdzdt[xdir].append((ref2[k,i,j]-ref[k,i,j])/90.)
#                        uu = u[k,i,j]
#                        vv = v[k,i,j]
#                        if uu>0:
#                            outdzdx[xdir].append((ref[k,i,j+1]-ref[k,i,j-1])/6000.)
#                        else:
#                            outdzdx[xdir].append((ref[k,i,j-1]-ref[k,i,j+1])/6000.)
#                        if vv>0:
#                            outdzdy[xdir].append((ref[k,i+1,j]-ref[k,i-1,j])/6000.)
#                        else:
#                            outdzdy[xdir].append((ref[k,i-1,j]-ref[k,i+1,j])/6000.)
#                        outdzdz[xdir].append((ref[k+1,i,j]-ref[k-1,i,j])/(dz[k+1]+dz[k]))
#                        outu[xdir].append(uu)
#                        outv[xdir].append(vv)
#                        outw[xdir].append(w[k,i,j])
#        outdzdt[xdir]=np.asarray(outdzdt[xdir])
#        outdzdx[xdir]=np.asarray(outdzdx[xdir])
#        outdzdy[xdir]=np.asarray(outdzdy[xdir])
#        outdzdz[xdir]=np.asarray(outdzdz[xdir])
#        outw[xdir]=np.asarray(outw[xdir])
#        outu[xdir]=np.asarray(outu[xdir])
#        outv[xdir]=np.asarray(outv[xdir])
#        print len(outv[xdir])

#    np.savez(time+'zbudget-dzdt.npz',**outdzdt)
#    np.savez(time+'zbudget-dzdx.npz',**outdzdx)
#    np.savez(time+'zbudget-dzdy.npz',**outdzdy)
#    np.savez(time+'zbudget-dzdz.npz',**outdzdz)
#    np.savez(time+'zbudget-u.npz',**outu)
#    np.savez(time+'zbudget-v.npz',**outv)
#    np.savez(time+'zbudget-w.npz',**outw)
