import numpy as np
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar
import glob

perts = pert75()
#
#wout = {}
#
#for p in perts:
#    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+p+'/'+p+'*'))
#    allw = []
#    for f in files:
#        allw.extend(getvar(f,'w'))
#    l=np.percentile(np.array(allw),99)
#    print p, l, np.max(np.array(allw))
#    wout[p]=l
#
#np.savez('w99.npz',**wout)

maxw = np.load('maxwpoints.npz')
w99 = np.load('w99.npz')

for p in perts:
    print p, maxw[p], w99[p]

v = np.zeros(75)
for i,k in enumerate(perts):
    v[i] = w99[k]
    order = np.argsort(v)
    vrank = []
    for i in range(75):
        vrank.append(perts[order[i]])
    vsort = sorted(v)

for p in vrank:
    print w99[p], maxw[p]



