import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import glob

def heatmap(xvar, yvar, outname):
	plt.hist2d(xvar, yvar)
	plt.savefig(outname)
	plt.clf()

names = ['revuintlatent','revuintabove10kmlatent','revuintabove5kmlatent','revuintabove8kmlatent']
files = []
for nam in names:
    files.append('/nobackup/rstorer/filesnpz/'+nam+'.npz')

var = []

maxw = np.load('../filesnpz/revumaxw.npz')

for i, fil in enumerate(files):
    xvar = []
    yvar = []
    latent = np.load(fil)
    for xdir in latent.keys():
	    l = latent[xdir]
	    w = maxw[xdir]
	    l = l[w>1]
	    w = w[w>1]
	    print l.max(), l.min()
	    print w.max(), w.min()
	    yvar.append(l[:])
	    xvar.append(w[:])
    xvar = np.concatenate(xvar)
    yvar = np.concatenate(yvar)

    plt.hist2d(xvar,yvar,bins = (100,100),cmap=mpl.cm.jet, norm=mpl.colors.LogNorm())
    plt.title(names[i])
    plt.savefig('../plots/latent-'+names[i]+'.png')
    plt.clf()
