import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar

def smoothedvar(var, i):
#    smoothvar = np.zeros((82,400))-40
    smoothvar = np.zeros((82,20))-40
#    smoothvar = np.zeros((82,33))-40
    var[var<-40] = -40
    for h in range(82):
#        for j in range(6,402,12):
#            ind = (j-6)/12
#            smoothvar[h,ind] = np.mean(var[h,i-6:i+6,j-6:j+6])
        for j in range(10,390,20):
            ind = (j-10)/20
            smoothvar[h,ind]=np.mean(var[h,i-10:i+10,j-10:j+10])
        #for j in range(10,390):
        #    smoothvar[h,j] = np.mean(var[h,i-10:i+10,j-10:j+10])
    return smoothvar

#testw = getvar('/nobackup/rstorer/convperts/growing/aug11-control/aug11-control-growing-057.h5','w')
#print testw.max(), np.unravel_index(testw.argmax(),testw.shape)

#testw = getvar('/nobackup/rstorer/convperts/mature/aug17-control/aug17-control-mature-004.h5','w')
#print testw.max(), np.unravel_index(testw.argmax(),testw.shape)

#testw = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-004.h5','w')
#print testw.max(), np.unravel_index(testw.argmax(),testw.shape)


w11 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/aug11-control/aug11-control-growing-057.h5','w'), 213)
w17 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/aug17-control/aug17-control-mature-004.h5','w'), 160)
w23 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-004.h5','w'), 170)
q11 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/quickbeam/aug11-control-growing-057-quickbeam.h5','reflectivity'), 213)
q17 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/aug17-control-mature-004-quickbeam.h5','reflectivity'), 160)
q23 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/feb23-control-mature-004-quickbeam.h5','reflectivity'), 170)
q112 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/quickbeam/aug11-control-growing-060-quickbeam.h5','reflectivity'), 213)
q172 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/aug17-control-mature-007-quickbeam.h5','reflectivity'), 160)
q232 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/feb23-control-mature-007-quickbeam.h5','reflectivity'), 170)


diff11 = (q112-q11)/1.5
diff17 = (q172-q17)/1.5
diff23 = (q232-q23)/1.5

diff11[q11 == -40] = -40
diff17[q17 == -40] = -40
diff23[q23 == -40] = -40

print diff11.max(), diff11.min()
print diff17.max(), diff17.min()
print diff23.max(), diff23.min()

ww11 = np.max(w11,0)
ww17 = np.max(w17,0)
ww23 = np.max(w23,0)

md11 = np.max(diff11,0)
md17 = np.max(diff17,0)
md23 = np.max(diff23,0)

z = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-004.h5','z_coords')/1000.
#x = np.arange(400)*.25
x = np.arange(20)*5
#x = np.arange(33)*3


height5km = np.argmin(np.abs(z-5))
www11 = np.max(w11[height5km:,:],0)
www17 = np.max(w17[height5km:,:],0)
www23 = np.max(w23[height5km:,:],0)

wmd11 = np.max(diff11[height5km:,:],0)
wmd17 = np.max(diff17[height5km:,:],0)
wmd23 = np.max(diff23[height5km:,:],0)


print w11.max(), np.unravel_index(w11.argmax(),w11.shape)
print w17.max(), np.unravel_index(w17.argmax(),w17.shape)
print w23.max(), np.unravel_index(w23.argmax(),w23.shape)


print q11.max(), np.unravel_index(q11.argmax(),q11.shape)
print q17.max(), np.unravel_index(q17.argmax(),q17.shape)
print q23.max(), np.unravel_index(q23.argmax(),q23.shape)

fig = plt.figure()

ax1 = plt.subplot(2,2,1)
ax1.plot(x,www11,linewidth=2,color='green')
ax1.plot(x,ww11,linewidth=2,color='blue',linestyle='dashed')
ax1.plot(x,wmd11,color='red',linewidth=2)
ax1.plot(x,md11,linestyle='dashed',color='black',linewidth=2)
ax1.set_ylim(0,15)
ax1.set_title('Aug 11')

ax1=plt.subplot(2,2,2)
ax1.plot(x,www17,linewidth=2,color='green')
ax1.plot(x,ww17,linewidth=2,color='blue',linestyle='dashed')
#plt.title('Max Updraft')
ax1.plot(x,wmd17,color='red',linewidth=2)
ax1.plot(x,md17,linestyle='dashed',color='black',linewidth=2)
ax1.set_ylim(0,15)
ax1.set_title('Aug 17')

ax1=plt.subplot(2,2,3)
ax1.plot(x,www23,linewidth=2,color='green',label = 'w above 5km')
ax1.plot(x,ww23,linewidth=2,color='blue',linestyle='dashed',label = 'w column')
ax1.plot(x,wmd23,color='red',linewidth=2, label = 'dBZ above 5km')
ax1.plot(x,md23,linestyle='dashed',color='black',linewidth=2, label = 'dBZ column')
ax1.set_title('Feb 23')
ax1.set_ylim(0,15)
plt.legend(bbox_to_anchor=(1.1,.3), loc="lower left")
plt.savefig('../plots/reflectivity_diff_w_5kmdegraded-4lines-dashedcolumn.png')

