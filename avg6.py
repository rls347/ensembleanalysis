import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar

w11 = getvar('/nobackup/rstorer/convperts/revu/aug11-control/aug11-control-revu-023.h5','w')
q11 = getvar('/nobackup/rstorer/convperts/revu/aug11-control/aug11-control-revu-023.h5','total_cond')

w17 = getvar('/nobackup/rstorer/convperts/revu/aug17-control/aug17-control-revu-023.h5','w')
q17 = getvar('/nobackup/rstorer/convperts/revu/aug17-control/aug17-control-revu-023.h5','total_cond')

w23 = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-023.h5','w')
q23 = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-023.h5','total_cond')

z = getvar('/nobackup/rstorer/convperts/revu/feb23-control/feb23-control-revu-016.h5','z_coords')/1000.
x = np.arange(400)*.25
fig = plt.figure()
plt.subplot(3,1,1)
meanw11=np.max(w11,1)
plt.contour(x,z,meanw11,levels=[2,5,10],colors='black')#,levels = np.linspace(0,48,9))
plt.ylabel('Aug 11',rotation=0,labelpad=30,fontweight='bold')
meanq11=np.mean(q11,1)
meanq11[meanq11<0.00035]=np.log(0)
plt.contourf(x,z,meanq11,cmap=plt.get_cmap('plasma'))
plt.title('Mean Condensate (g/kg)')
plt.colorbar()
plt.xticks([])
plt.ylim(0,20)
plt.subplot(3,1,2)
meanw17=np.max(w17,1)
plt.contour(x,z,meanw17,levels=[2,5,10],colors='black')#, levels = np.linspace(0,9,9))
plt.ylabel('Aug 17',rotation=0,labelpad=30,fontweight='bold')
meanq17=np.mean(q17,1)
meanq17[meanq17<0.00035]=np.log(0)
plt.contourf(x,z,meanq17,cmap=plt.get_cmap('plasma'))
plt.colorbar()
plt.xticks([])
plt.ylim(0,20)
plt.subplot(3,1,3)
meanw23=np.max(w23,1)
plt.contour(x,z,meanw23,levels=[2,5,10],colors='black')#,levels = np.linspace(0,28,9))
plt.ylabel('Feb 23',rotation=0,labelpad=30,fontweight='bold')
meanq23=np.mean(q23,1)
meanq23[meanq23<0.00035]=np.log(0)
plt.contourf(x,z,meanq23,cmap=plt.get_cmap('plasma'))
plt.ylim(0,20)
plt.xlabel('km')
plt.colorbar()
fig.tight_layout()
plt.savefig('panel6-mean-time23.png')
plt.clf()




