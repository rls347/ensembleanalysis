import numpy as np
import copy
from rachelutils.hdfload import getvar,getrho,getdz
from rachelutils.dumbnaming import pert75
import glob


totpcp = np.load('../filesnpz/totpcpmm.npz')

modeldirs = ['feb23-control','aug11-control','aug17-control']
for xdir in modeldirs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nt = len(files)

    nuc = np.zeros(nt)
    cond = np.zeros(nt)
    evap = np.zeros(nt)
    q = np.zeros(nt)
    pcp = np.zeros(nt)
    vap = np.zeros(nt)

    dz = getdz(files[0])
    rho = getrho(files[0])[:,0,0]
    for i in range(nt):
        fil = files[i]
        var = (getvar(fil,'vapliqt')+getvar(fil,'vapicet')) * rho[:,None,None] * dz[:,None,None]
        n = getvar(fil,'nuccldrt')+getvar(fil,'nucicert')* rho[:,None,None] * dz[:,None,None]
        t = getvar(fil,'total_cond')* rho[:,None,None] * dz[:,None,None]
        p = getvar(fil,'totpcp')*1000.
        v = getvar(fil,'vapor')* rho[:,None,None] * dz[:,None,None]

        pos = copy.deepcopy(var)
        neg = copy.deepcopy(var)
        pos[pos<0]=0.
        neg[neg>0]=0.

        q[i] = np.mean(t)
        nuc[i] = np.mean(n)
        evap[i] = np.mean(neg)
        cond[i] = np.mean(pos)
        pcp[i] = np.mean(p)
        vap[i] = np.mean(v)
        if i == nt-1:
            print 'tot', np.sum(p)/1000.
    print xdir
    print 'source', np.sum(cond[1:]) + np.sum(evap[1:]) + np.sum(nuc[1:])
    print 'q', q[-1]-q[0]
    print 'pcp', pcp[-1]-pcp[0],totpcp[xdir]










