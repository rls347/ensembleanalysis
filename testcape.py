import matplotlib
matplotlib.use("Agg")
import numpy as np
from rachelutils.hdfload import getvar
from rachelutils.thermo import get_cape, satmixratio
from rachelutils.dumbnaming import pert75
import matplotlib.pyplot as plt

prevcape = np.load('../filesnpz/cape.npz')

dirs = pert75()

prev = np.zeros(75)
new = np.zeros(75)

mix = {}
sfc = {}
mu = {}

for i, xdir in enumerate(dirs):
    filename = '/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5'
    capemixed,parcel = get_cape(filename,'mixed')
    capesfc, parcel = get_cape(filename, 'sfc')
    capemu, parcel = get_cape(filename, 'mu')
    print xdir, capemixed, capesfc, capemu, prevcape[xdir]
    prev[i] = prevcape[xdir]
    new[i]= capemixed
    mix[xdir]=capemixed
    sfc[xdir]=capesfc
    mu[xdir]=capemu

ln = np.arange(3500)
plt.scatter(prev, new)
plt.plot(ln,ln)
plt.xlabel('ncl calc')
plt.ylabel('my code')
plt.savefig('capecompare.png')
plt.clf()

np.savez('../filesnpz/cape_mu.npz', **mu)
np.savez('../filesnpz/cape_mixed.npz',**mix)
np.savez('../filesnpz/cape_sfc.npz', **sfc)
