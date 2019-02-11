import numpy as np
from rachelutils.hdfload import getvar
import glob


files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/feb23-control/*h5'))
rate = 0.
kg = 0.
for f in files:
    rate = rate+(getvar(f,'pcprate')*(5./60))
    tot = getvar(f,'totpcp')
    kg = kg+getvar(f,'pcpg')
    print np.sum(rate),'   ', np.sum(tot), '   ', np.sum(kg)


var = np.load('../filesnpz/totpcpmm.npz')
print var['feb23-control']
