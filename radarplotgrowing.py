import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar

def smoothedvar(var, i):
#    smoothvar = np.zeros((82,400))-40
#    smoothvar = np.zeros((82,20))-40
    smoothvar = np.zeros((82,33))-40
    var[var<-40] = -40
    for h in range(82):
        for j in range(6,402,12):
            ind = (j-6)/12
            smoothvar[h,ind] = np.mean(var[h,i-6:i+6,j-6:j+6])
#        for j in range(10,390,20):
#            ind = (j-10)/20
#            smoothvar[h,ind]=np.mean(var[h,i-10:i+10,j-10:j+10])
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
tc11 = getvar('/nobackup/rstorer/convperts/growing/aug11-control/aug11-control-growing-057.h5','total_cond')
#tc11[tc11>0.001]=1
tc17 = getvar('/nobackup/rstorer/convperts/mature/aug17-control/aug17-control-mature-004.h5','total_cond')
#tc17[tc17>0.001]=1
tc23 = getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-004.h5','total_cond')
#tc23[tc23>0.001]=1
cond11 = smoothedvar(tc11,213)
cond17 = smoothedvar(tc17,160)
cond23 = smoothedvar(tc23,170)
#cond11 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/aug11-control/aug11-control-growing-057.h5','total_cond'), 213)
#cond17 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/aug17-control/aug17-control-mature-004.h5','total_cond'), 160)
#cond23 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-004.h5','total_cond'), 170)
q11 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/quickbeam/aug11-control-growing-057-quickbeam.h5','reflectivity'), 213)
q17 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/aug17-control-mature-004-quickbeam.h5','reflectivity'), 160)
q23 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/feb23-control-mature-004-quickbeam.h5','reflectivity'), 170)
q112 = smoothedvar(getvar('/nobackup/rstorer/convperts/growing/quickbeam/aug11-control-growing-060-quickbeam.h5','reflectivity'), 213)
q172 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/aug17-control-mature-007-quickbeam.h5','reflectivity'), 160)
q232 = smoothedvar(getvar('/nobackup/rstorer/convperts/mature/quickbeam/feb23-control-mature-007-quickbeam.h5','reflectivity'), 170)

cond11[cond11<.001]=0
cond17[cond17<.001]=0
cond23[cond23<.001]=0

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
#x = np.arange(20)*5
x = np.arange(33)*3


height5km = np.argmin(np.abs(z-5))
www11 = np.max(w11[height5km:,:],0)
www17 = np.max(w17[height5km:,:],0)
www23 = np.max(w23[height5km:,:],0)

md11 = np.max(diff11[height5km:,:],0)
md17 = np.max(diff17[height5km:,:],0)
md23 = np.max(diff23[height5km:,:],0)


print w11.max(), np.unravel_index(w11.argmax(),w11.shape)
print w17.max(), np.unravel_index(w17.argmax(),w17.shape)
print w23.max(), np.unravel_index(w23.argmax(),w23.shape)


print q11.max(), np.unravel_index(q11.argmax(),q11.shape)
print q17.max(), np.unravel_index(q17.argmax(),q17.shape)
print q23.max(), np.unravel_index(q23.argmax(),q23.shape)

fig = plt.figure()
ax7 = plt.subplot(3,3,1)
#ax7.contourf(x,z,cond11,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax7.contour(x,z,cond11,levels = [0,.001,20],colors = 'gray')
ax7.contourf(x,z,q11,levels=np.linspace(-30,40,20))
ax7.set_ylabel('Height (km)')
ax7.set_title('Aug 11',size=14,fontweight='bold')
ax7.set_ylim(0,20)
ax7.tick_params(labelbottom='off')

ax8=plt.subplot(3,3,2)
#ax8.contourf(x,z,cond17,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax8.contour(x,z,cond17,levels = [0,.001,20],colors = 'gray')
ax8.contourf(x,z,q17,levels=np.linspace(-30,40,20))
ax8.set_ylim(0,20)
ax8.set_title('Aug 17',size = 14, fontweight='bold')
ax8.tick_params(labelbottom = 'off')
ax8.tick_params(labelleft= 'off')

ax9=plt.subplot(3,3,3)
#ax9.contourf(x,z,cond23,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax9.contour(x,z,cond23,levels = [0,.001,20],colors = 'gray')
rc =ax9.contourf(x,z,q23,levels=np.linspace(-30,40,20))
ax9.set_ylim(0,20)
ax9.set_title('Feb 23', fontweight = 'bold')
ax9.tick_params(labelbottom = 'off')
ax9.tick_params(labelleft= 'off')


ax4=plt.subplot(3,3,4)
#ax4.contourf(x,z,cond11,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax4.contour(x,z,cond11,levels = [0,.001,20],colors = 'gray')
dc = ax4.contourf(x,z,diff11,levels=np.linspace(-15,15,20))
ax4.set_ylabel('Height (km)')
#plt.title('Reflectivity Diff')
ax4.set_ylim(0,20)
ax4.tick_params(labelbottom='off')

ax5 = plt.subplot(3,3,5)
#ax5.contourf(x,z,cond17,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax5.contour(x,z,cond17,levels = [0,.001,20],colors = 'gray')
ax5.contourf(x,z,diff17,levels=np.linspace(-15,15,20))
ax5.set_ylim(0,20)
ax5.tick_params(labelbottom='off')
ax5.tick_params(labelleft='off')
#plt.title('Reflectivity Diff')

ax5 = plt.subplot(3,3,6)
#ax5.contourf(x,z,cond23,levels = [0,.001,20],colors = ['white','lightgray','white'])
#ax5.contour(x,z,cond23,levels = [0,.001,20],colors = 'gray')
ax5.contourf(x,z,diff23,levels=np.linspace(-15,15,20))
ax5.set_ylim(0,20)
ax5.tick_params(labelbottom='off')
ax5.tick_params(labelleft='off')

ax1 = plt.subplot(3,3,7)
ax1.plot(x,www11,linewidth=2,color='blue')
#plt.title('Max Updraft')
ax1.set_xlabel('km')
ax1.set_ylabel('Max W (m/s)')
ax1.set_ylim(0,10)
ax2 = ax1.twinx()
ax2.plot(x,md11,linestyle='dashed',color='black',linewidth=2)
ax2.set_ylim(0,15)
ax2.tick_params(labelright='off')
#ax2.yaxis.tick_right()
#ax2.yaxis.set_label_position("right")

ax1=plt.subplot(3,3,8)
ax1.plot(x,www17,linewidth=2)
ax1.tick_params(labelleft='off')
ax1.set_ylim(0,10)
ax1.set_yticklabels([])
ax1.set_xlabel('km')
#plt.title('Max Updraft')
ax2 = ax1.twinx()
ax2.plot(x,md17,linestyle='dashed',color='black',linewidth=2)
ax2.set_ylim(0,15)
ax2.tick_params(labelright='off')
ax2.tick_params(labelleft='off')


ax1=plt.subplot(3,3,9)
ax1.plot(x,www23,linewidth=2)
ax1.tick_params(labelleft='off')
ax1.set_yticklabels([])
ax1.set_ylim(0,10)
ax1.set_xlabel('km')
#plt.title('Max Updraft')
ax2 = ax1.twinx()
ax2.plot(x,md23,linestyle='dashed',color='black',linewidth=2)
ax2.set_ylim(0,15)
ax2.set_ylabel('Max dBZ/min')
ax2.tick_params(labelleft='off')


fig.subplots_adjust(right = .8)
ax4 = fig.add_axes([.84,0.68,0.02,0.2],frameon=False, xticks=[], yticks=[])
fig.colorbar(rc, cax=ax4,ticks = [-30,-20,-10,0,10,20,30,40],label = 'dBZ' )
ax5 = fig.add_axes([.84,.4,.02,.2],frameon=False, xticks=[], yticks=[])
fig.colorbar(dc, cax=ax5, ticks = [-15,0,15],label = 'dBZ/min')
#fig.tight_layout()
#plt.suptitle('5km footprint, both ddBZ and w above 5km')
plt.savefig('../plots/reflectivity_diff_w_3kmdegraded-deldbz5km_w5km.png')


