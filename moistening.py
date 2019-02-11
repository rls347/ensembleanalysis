import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.collections import LineCollection
from rachelutils.dumbnaming import pert75

def getrh(fil):
    heights = getvar(fil,'z_coords')[1:]
    tempk = np.mean(np.mean(getvar(fil,'tempk')[1:,:,:],1),1)
    press = np.mean(np.mean(getvar(fil,'press')[1:,:,:],1),1)
    vapor = np.mean(np.mean(getvar(fil,'vapor')[1:,:,:],1),1)
    rho = (press*100.)/ (287.*tempk)
    dz = getdz(fil)[:-1]

    es = 611.2*np.exp(17.67*(tempk-273.15)/(tempk-29.65))
    rvs = 622*es/((press*100.)-es)

    vsat = rvs * rho * dz
    vact = vapor * rho * dz

    lows = np.where(press > 850.)
    mids = np.logical_and(press < 850, press > 500)
    highs = np.where(press < 500)

    lowsat = np.sum(vact[lows])#100. * (np.sum(vact[lows]) / np.sum(vsat[lows]))
    midsat = np.sum(vact[mids])#100. * (np.sum(vact[mids]) / np.sum(vsat[mids]))
    highsat = np.sum(vact[highs])#100. * (np.sum(vact[highs]) / np.sum(vsat[highs]))
    allsat = np.sum(vact)#100. * (np.sum(vact) / np.sum(vsat))

    return lowsat,midsat,highsat,allsat




modeldirs = pert75()
rhall = np.load('../filesnpz/rhlow.npz')

lowlow = []
midmid = []
toptop = []
allall = []

for xdir in modeldirs:
    print xdir
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/*h5'))
    nf = len(files)
    lowsat = np.zeros(nf)
    midsat = np.zeros(nf)
    highsat = np.zeros(nf)
    allsat = np.zeros(nf)
    for i, f in enumerate(files):
        #lowsat[i],midsat[i],highsat[i],allsat[i] = getrh(f)
        allsat[i] = np.mean(getvar(f,'vertint_vapor'))

    xs = np.arange(nf)*5
#    lowlow.append((xs,lowsat))
#    midmid.append((xs,midsat))
#    toptop.append((xs,highsat))
    allall.append((xs,allsat))


rh = np.zeros(75)
for i in range(75):
    rh[i] = rhall[modeldirs[i]]
#linest = [zip(x,y) for x, y in lowlow]
#fig, ax = plt.subplots()
#lines = LineCollection(linest, array = rh, cmap = plt.cm.rainbow, linewidth=3)
#ax.add_collection(lines)
#fig.colorbar(lines)
#ax.autoscale()
#plt.savefig('../plots/timeseriesintvap-low.png')
#plt.clf()
#
#line2 = [zip(x,y) for x, y in midmid]
#fig, ax = plt.subplots()
#lines2 = LineCollection(line2, array = rh, cmap = plt.cm.rainbow, linewidth=3)
#ax.add_collection(lines2)
#fig.colorbar(lines2)
#ax.autoscale()
#plt.savefig('../plots/timeseriesintvap-mid.png')
#plt.clf()
#
#line1 = [zip(x,y) for x, y in toptop]
#fig, ax = plt.subplots()
#lines1 = LineCollection(line1, array = rh, cmap = plt.cm.rainbow, linewidth=3)
#ax.add_collection(lines1)
#fig.colorbar(lines1)
#ax.autoscale()
#plt.savefig('../plots/timeseriesintvap-high.png')
#plt.clf()
#
line3 = [zip(x,y) for x, y in allall]
fig, ax = plt.subplots()
lines3 = LineCollection(line3, array = rh, cmap = plt.cm.rainbow, linewidth=3)
ax.add_collection(lines3)
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Column Water Vapor (mm)')
fig.colorbar(lines3)
ax.autoscale()
plt.savefig('../plots/timeseriesintvap-column.png')
plt.clf()









