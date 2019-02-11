import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar, getdz
import glob
from matplotlib.colors import LogNorm
from rachelutils.dumbnaming import pert75,case25


dirs = pert75()
dirs = ['aug17-control','feb23-control','aug11-control']

#times = ['growing','mature']
lab= ['5km','8km','10km']
times = ['mature5km','mature8km','mature10km']
#namenums = ['23000','33000','40000','46000','50000','54000']
namenums = [1]
nameheights = ['2000','4000','6000','8000','10000','12000']
labelname = ['2km','4km','6km','8km','10km','12km']
colors = ['blue','red','green','black','purple','orange']
for tim,time in enumerate(times):
    for namename in  namenums:
        outdzdt = np.load(time+'zbudget-dzdt-control.npz')
        outdzdx = np.load(time+'zbudget-dzdx-control.npz')
        outdzdy = np.load(time+'zbudget-dzdy-control.npz')
        outdzdz = np.load(time+'zbudget-dzdz-control.npz')
        outu = np.load(time+'zbudget-u-control.npz')
        outv = np.load(time+'zbudget-v-control.npz')
        outw = np.load(time+'zbudget-w-control.npz')

        allyterm = []
        allxterm = []
        allzterm = []
        allalpha = []
        alltterm = []
        allcterm = []
        allw = []
        allalpha = []

        for xdir in dirs:
            w = outw[xdir]
            print w.shape
            u = outu[xdir]
            v = outv[xdir]
            dzdt = outdzdt[xdir]
            dzdx = outdzdx[xdir]
            dzdy = outdzdy[xdir]
            dzdz = outdzdz[xdir]

            dzdz = dzdz[dzdt>0]
            dzdy = dzdy[dzdt>0]
            dzdx = dzdx[dzdt>0]
            u = u[dzdt>0]
            v = v[dzdt>0]
            w = w[dzdt>0]
            dzdt = dzdt[dzdt>0]

            allw.extend(w)
            allxterm.extend(u*dzdx)
            allyterm.extend(v*dzdy)
            allzterm.extend(w*dzdz)
            alltterm.extend(dzdt)
            c = dzdt+(u*dzdx+v*dzdy+w*dzdz)
            allcterm.extend(c)
            alpha = ((dzdt+u*dzdx+v*dzdy)/w) + dzdz
            allalpha.extend(alpha)

        allyterm = np.asarray(allyterm)
        allxterm = np.asarray(allxterm)
        allzterm = np.asarray(allzterm)
        alltterm = np.asarray(alltterm)
        allcterm = np.asarray(allcterm)
        allw = np.asarray(allw)
        allalpha = np.asarray(allalpha)

        print allcterm.shape
        terms = ['dZ/dt','u dZ/dx','v dZ/dy', 'w dZ/dz', 'C']
        x_pos = np.arange(len(terms))
        means = [np.mean(alltterm),np.mean(allxterm),np.mean(allyterm),np.mean(allzterm),np.mean(allcterm)]
        stds = [np.std(alltterm),np.std(allxterm),np.std(allyterm),np.std(allzterm),np.std(allcterm)]
        maxs = [np.max(alltterm),np.max(allxterm),np.max(allyterm),np.max(allzterm),np.max(allcterm)]
        mins = [np.min(alltterm),np.min(allxterm),np.min(allyterm),np.min(allzterm),np.min(allcterm)]
        
        fig, ax = plt.subplots()
        ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_xticks(x_pos)
        ax.set_ylabel('dBZ/s')
        ax.set_title('Reflectivity Budget Terms')
        ax.set_xticklabels(terms)
        ax.yaxis.grid(True)

        plt.tight_layout()
        
        plt.savefig(time+'zbudgetbar-modelres.png')
        plt.clf()

        allvars = [alltterm,allxterm,allyterm,allzterm,allcterm]
        plt.boxplot(allvars,showfliers=False,labels = terms)
        plt.axhline(color='gray',linestyle='dashed') 
        plt.title('Reflectivity Budget Terms z= '+lab[tim] )
        plt.ylabel('dBZ/s')
        plt.savefig(time+'zbudget-boxplot-modelres.png')
        plt.clf()




        xvar = alltterm+allxterm+allyterm
        xd = np.asarray(allw)
        yd = np.asarray(xvar)

        plt.scatter(xd, yd, s=30, alpha=0.15, marker='o',color='blue')
        par = np.polyfit(xd, yd, 1, full=True)

        slope=par[0][0]
        intercept=par[0][1]
        xl = [min(xd), max(xd)]
        yl = [slope*xx + intercept  for xx in xl]

        variance = np.var(yd)
        residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(xd,yd)])
        Rsqr = np.round(1-residuals/variance, decimals=2)
        pos1 = np.max(xl)*.75-np.min(xl)
        pos2 = np.max(yl)*.75-np.min(yl)
        plt.text(10,pos2,'$R^2 = %0.2f$'% Rsqr +'  slope = $%.4f$'% slope,color = 'black')
        plt.plot(xl, yl,linewidth=2,color='black')
    plt.xlabel("Vertical Velocity (m/s)")
    plt.ylabel("dZ/dt + u dZ/dx + v dZ/dy (dbz/s)")
    plt.legend(loc = 'upper center')
    plt.savefig(time+'scatter-wvsc-fit-modelres.png')
    plt.savefig(time+'scatterdbz-w-fit-modelres.png')
    plt.clf()



