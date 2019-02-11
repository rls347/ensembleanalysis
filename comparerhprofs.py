import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import glob
from rachelutils.hdfload import meanprof,getvar
from rachelutils.dumbnaming import case25,pert75


def rankvar(var,dirs):
    nv = len(dirs)
    v = np.zeros(nv)
    for i,k in enumerate(dirs):
        v[i] = var[k]
    order = np.argsort(v)
    vrank = []
    for i in range(nv):
        vrank.append(dirs[order[i]])
    vsort = sorted(v)
    return vsort,vrank

cases = case25()
names = pert75()

rhprofsinit = {}
vapprofsinit = {}
rhprofsfinal = {}
vapprofsfinal = {}
rhdiffs = {}
vapdiffs = {}
tinit = {}
tfinal = {}
tdiff = {}

tlow = {}
thigh = {}
vlow = {}
vhigh = {}


pcp = np.load('maxwpoints.npz')
onecase = ['aug11','aug17','feb23']
for c in range(3):
    casename = onecase[c]
    names = cases[c]

    tlow[casename] = []
    thigh[casename] = []
    vlow[casename] = []
    vhigh[casename] = []

    vsort,vrank = rankvar(pcp,names)
    print vrank[0:6],vrank[-6:]

    for run in names:
        files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+run+'/'+run+'*h5'))
        f1 = files[0]
        f2 = files[-1]
        rhprofsinit[run] = meanprof(f1,'relhum')
        rhprofsfinal[run] = meanprof(f2,'relhum')
        vapprofsinit[run] = meanprof(f1,'vapor')
        vapprofsfinal[run] = meanprof(f2,'vapor') 
        tinit[run] = meanprof(f1,'tempk')
        tfinal[run] = meanprof(f2,'tempk')
        tdiff[run] = tfinal[run]-tinit[run]
        rhdiffs[run] = rhprofsfinal[run]-rhprofsinit[run]
        vapdiffs[run] = vapprofsfinal[run]-vapprofsinit[run]



    height = getvar(files[0],'z_coords')/1000.


    lowvaps = np.zeros_like(height)
    lowrhs = np.zeros_like(height)
    highvaps = np.zeros_like(height)
    highrhs = np.zeros_like(height)

    difflowvaps = np.zeros_like(height)
    difflowrhs = np.zeros_like(height)
    diffhighvaps = np.zeros_like(height)
    diffhighrhs = np.zeros_like(height)
    difflowtemp = np.zeros_like(height)
    diffhightemp = np.zeros_like(height)

    ct = 0.0
    for i in range(6):
        lowvaps = lowvaps + vapprofsinit[vrank[i]]
        lowrhs = lowrhs + rhprofsinit[vrank[i]]
        highvaps = highvaps + vapprofsinit[vrank[-1*i]]
        highrhs = highrhs + rhprofsinit[vrank[-1*i]]
        difflowvaps = difflowvaps + vapdiffs[vrank[i]]
        difflowrhs = difflowrhs + rhdiffs[vrank[i]]
        diffhighvaps = diffhighvaps + vapdiffs[vrank[-1*i]]
        diffhighrhs = diffhighrhs + rhdiffs[vrank[-1*i]]
        difflowtemp = difflowtemp + tdiff[vrank[i]]
        diffhightemp = diffhightemp + tdiff[vrank[-1*i]]
        ct = ct + 1.0

    lowvaps = lowvaps/ct
    lowrhs = lowrhs/ct
    highvaps = highvaps/ct
    highrhs = highrhs/ct
    difflowvaps = difflowvaps/ct
    difflowrhs = difflowrhs/ct
    diffhighvaps = diffhighvaps/ct
    diffhighrhs = diffhighrhs/ct
    difflowtemp = difflowtemp/ct
    diffhightemp = diffhightemp/ct


    for i in range(6):
        tlow[casename].append(rhdiffs[vrank[i]])
        thigh[casename].append(rhdiffs[vrank[-1*i]])

    



fig = plt.figure()
ax = fig.add_subplot(1,3,1)
for i in range(6):
    ax.plot(tlow['aug11'][i],height,color='cornflowerblue')
    ax.plot(thigh['aug11'][i],height,color='firebrick')
ax.set_ylim(0,18)
ax.set_title('Aug 11',fontweight='bold')
plt.xticks(size=11)
plt.ylabel('Height (km)')
plt.xlabel('RH diff')
plt.yticks(size=11)

ax = fig.add_subplot(1,3,2)
for i in range(6):
    ax.plot(tlow['aug17'][i],height,color='cornflowerblue')
    ax.plot(thigh['aug17'][i],height,color='firebrick')
ax.set_ylim(0,18)
ax.set_title('Aug 17',fontweight='bold')
#plt.xticks([-0.4,0.0,0.4,0.8,1.2],size=10)
plt.xticks(size=11)
plt.xlabel('RH diff')
plt.yticks(size=11)

ax = fig.add_subplot(1,3,3)
for i in range(6):
    ax.plot(tlow['feb23'][i],height,color='cornflowerblue')
    ax.plot(thigh['feb23'][i],height,color='firebrick')
ax.set_ylim(0,18)
ax.set_title('Feb 23',fontweight='bold')
#plt.xticks([-1,0,1,2],size=10)
plt.xticks(size=11)
plt.xlabel('RH diff')
plt.yticks(size=11)

#plt.tight_layout()
plt.savefig('rhdiffpanels-bymaxw.png')
plt.close(fig)









