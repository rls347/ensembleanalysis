import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import Polygon
from rachelutils.dumbnaming import pert75,case25

def dots(ydots, xdots, ytitle,yvar,xtitle,xvar):
    plt.scatter(xdots,ydots)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.savefig('boxdots_'+xvar+'_'+yvar+'.png')
    plt.clf()


def boxdots(t,xtitle,xvar,ytitle,yvar,ax=None):
    if ax is None:
        ax = plt.gca()
    xvals = np.zeros(36)
    yvals = np.zeros(36)
    colors = ['cornflowerblue','firebrick','cornflowerblue','firebrick','cornflowerblue','firebrick']
    allc = []
    for i in range(6):
        xvals[i*6:i*6+6]=i+1
        yvals[i*6:i*6+6]=t[i][:]
        for bu in range(6):
            allc.append(colors[i])
    bp = ax.scatter(xvals,yvals,c=allc,edgecolor=allc)
    ax.set_title(ytitle, size=12)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', length =0)
    ax.tick_params(axis='y', length=0)
    if yvar == 'rh-press-850-500':
        ax.set_ylim(76,92)
    plt.xticks([1.5, 3.5, 5.5], ['Aug11', 'Aug17', 'Feb23'],size=8)
    plt.yticks(size=9)
    return bp
    
def boxer(t,xtitle,xvar,ytitle,yvar,ax=None):
    if ax is None:
        ax = plt.gca()

    bp=ax.boxplot(t)
#    ax.set_xlabel(xtitle)
    ax.set_title(ytitle,size=12)
#    ax.set_title()
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', length =0)
    ax.tick_params(axis='y', length=0)

#    colors = ['m','m','c','c','y','y']
    colors = ['cornflowerblue','firebrick','cornflowerblue','firebrick','cornflowerblue','firebrick']

    print len(bp['boxes'])
    print len(bp['whiskers'])
    print len(bp['fliers'])

    for i in range(0, len(bp['boxes'])):
        bp['boxes'][i].set_color(colors[i])
       # we have two whiskers!
        bp['whiskers'][i*2].set_color(colors[i])
        bp['whiskers'][i*2 + 1].set_color(colors[i])
        bp['whiskers'][i*2].set_linewidth(2)
        bp['whiskers'][i*2 + 1].set_linewidth(2)
       # top and bottom fliers
       # (set allows us to set many parameters at once)
        bp['fliers'][i].set(markerfacecolor=colors[i],
                       marker='o', alpha=0.75, markersize=2,
                       markeredgecolor='none')
#        bp['fliers'][i * 2 + 1].set(markerfacecolor=colors[i],
#                       marker='o', alpha=0.75, markersize=6,
#                       markeredgecolor='none')
        bp['medians'][i].set_color('black')
        bp['medians'][i].set_linewidth(1)
       # and 4 caps to remove
        for c in bp['caps']:
            c.set_linewidth(0)
        box = bp['boxes'][i]
        box.set_linewidth(0)
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor = colors[i], linewidth=0)
            ax.add_patch(boxPolygon)
    plt.xticks([1.5, 3.5, 5.5], ['Aug11', 'Aug17', 'Feb23'],size=9)
    plt.yticks(size=10)
#    plt.savefig('boxplot_'+yvar+'_sortedby_'+xvar+'.png')
    return bp
#    plt.clf()
#    plt.close(fig)




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

def orderbysort(vrank,var):
    nv = len(vrank)
    v = np.zeros(nv)
    for i in range(nv):
        v[i] = var[vrank[i]]
    return v
files = [
    'convprecipfrac.npz',
    'maxwpoints.npz',
    'totpcpmm.npz',
    'cape_ML.npz',
    'shear.npz',
    'rhlow.npz',
    'maxpcprate.npz',
    'pcprate99.npz',
    'lapserate2z_freezing4-6.npz',
    'lapserate2z_below4.npz',
    'rh-press-500-100.npz',
    'colvap-press-500-100.npz',
    'rh-press-950-750.npz',
    'colvap-press-950-750.npz',
    'rh-z-0-2000.npz',
    'colvap-z-0-2000.npz',
    'rh-z-2000-4000.npz',
    'colvap-z-2000-4000.npz']

#xfiles = ['totpcpmm.npz','maxpcprate.npz','pcprate99.npz','convprecipfrac.npz','maxwpoints.npz']
#xvars = ['Total Precip (mm)','Max Precip Rate (mm/hr)','99th % Precip Rate','Convective Precip Fraction','Max Updraft Speed']
#xnames = ['totpcpmm','maxpcprate','pcprate99','convprecipfrac','maxwpoints']

xfiles = ['maxwpoints.npz']
xvars = ['99th Percentile Rain Rate']
xnames = ['pcp99']

yfiles = ['cape_ML.npz','shear.npz','cin.npz','ltss.npz','colvap-press-1000-100.npz',
    'rh-press-1000-850.npz',
    'rh-press-850-500.npz',
    'rh-press-500-100.npz']
#yvars = ['CAPE (J/kg)','850-350mb Shear (m/s)', 'Low Level Max Lapse Rate (K/km)','Lower Tropospheric Stability (K)',
#    'Freezing Level Max Lapse Rate (K/km)','Column Water Vapor',
#    '1000-850mb Relative Humidity',
#    '500-100mb Relative Humidity',
#    '850-500mb Relative Humidity']


yvars = ['CAPE','Shear','CIN','LTSS','PWAT','Low Trop RH','Mid Trop RH','Upper Trop RH']

ynames = ['cape_ML','shear','CIN','ltss','colvap-press-1000-100',
    'rh-press-1000-850','rh-press-850-500','rh-press-500-100']

alldirs = case25()
for c in range(3):
    dirs = alldirs[c]

fig = plt.figure()    
for i in range(len(xfiles)):
    xvar = np.load(xfiles[i])
    xdots = np.array([xvar[f] for f in xvar.keys()])
    for j in range(len(yfiles)):
        print i, j, xnames[i],ynames[j]
        yvar = np.load(yfiles[j])
        ydots = np.array([yvar[f] for f in yvar.keys()])
        t=[]
        for c in range(3):
            dirs = alldirs[c]
            xsort,xrank = rankvar(xvar,dirs)
            yvar = np.load(yfiles[j])
            yrank = orderbysort(xrank,yvar)
            t.append(yrank[0:6])
            t.append(yrank[-6:])

#        dots(xdots,ydots,xvars[i],xnames[i],yvars[j],ynames[j])
        ax = fig.add_subplot(4,4,j+1)
#        tf = boxer(t,xvars[i],xnames[i],yvars[j],ynames[j],ax)
        tf = boxdots(t,xvars[i],xnames[i],yvars[j],ynames[j],ax)
#plt.suptitle('Quartiles of 99th Percentile Rain Rate')
plt.tight_layout()
plt.savefig('panel8-maxw-dots.png')
plt.clf()











