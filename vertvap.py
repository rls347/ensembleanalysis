import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

modeldirs = pert75()

initval = {}

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nf = len(files)
    f = files[0]
    v = getvar(f,'vertint_vapor')
    initval[xdir] =np.mean(v)

    print xdir,initval[xdir]

np.savez('../filesnpz/init_vertintvap.npz',**initval)


