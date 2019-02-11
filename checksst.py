import numpy as np
from rachelutils.hdfload import getvar
import glob
from rachelutils.dumbnaming import pert75

runs=pert75()
for dir in runs:
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+dir+'/'+dir+'*'))
    print dir
    f=files[1]
    s=getvar(f,'rshort')
    print s.max(), s.min(), s.mean()
    f=files[-1]
    s=getvar(f,'rshort')
    print s.max(), s.min(), s.mean()

#files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/aug11-control/aug*'))
#for f in files:
#    s=getvar(f,'albedt')
#    print s.max(), s.min(), s.mean()
