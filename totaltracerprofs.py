import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75
from rachelutils.hdfload import getvar,getdz,getrho
import glob

def plot2d5panel(xdir,var1,var2,var3,var4,var5):
    height = getvar('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5','z_coords')/1000.
    xs = np.arange(var1.shape[1])*5
    m = np.argmin(np.abs(height-5))
    var1[:m,:]=np.min(var1[m:,:])
    var2[:m,:]=np.min(var2[m:,:])
    var3[:m,:]=np.min(var3[m:,:])
    var4[:m,:]=np.min(var4[m:,:])
    var5[:m,:]=np.min(var5[m:,:])
    
    plt.subplot(1,5,1)
    plt.contourf(xs,height,var1,levels=np.linspace(var1.min(),var1.max(),20))
    plt.title('0-2 km')
    plt.xlabel('Time (min)')
    plt.ylabel('Height (km)')
    plt.ylim(5,18)
    plt.colorbar()

    plt.subplot(1,5,2)
    plt.contourf(xs,height,var2,levels=np.linspace(var2.min(),var2.max(),20))
    plt.title('2-4 km')
    plt.xlabel('Time (min)')
    plt.yticks([])
    plt.ylim(5,18)
    plt.colorbar()

    plt.subplot(1,5,3)
    plt.contourf(xs,height,var3,levels=np.linspace(var3.min(),var3.max(),20))
    plt.title('4-6 km')                                     
    plt.xlabel('Time (min)')                                    
    plt.yticks([])                                                  
    plt.ylim(5,18)                                                      
    plt.colorbar()

    plt.subplot(1,5,4)
    plt.contourf(xs,height,var4,levels=np.linspace(var4.min(),var4.max(),20))
    plt.title('6-8 km')                                     
    plt.xlabel('Time (min)')                                    
    plt.yticks([])                                                  
    plt.ylim(5,18)                                                      
    plt.colorbar()

    plt.subplot(1,5,5)
    plt.contourf(xs,height,var5,levels=np.linspace(var5.min(),var5.max(),20))
    plt.title('8-10 km')                                     
    plt.xlabel('Time (min)')                                    
    plt.yticks([])                                                  
    plt.ylim(5,18)                                                      
    plt.colorbar()

    plt.suptitle(xdir)
    plt.savefig('surfacetracers5panel-'+xdir+'.png')
    plt.clf()



def plot2d2panel(xdir,var1,var2,rh0,rh1):
    height = getvar('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5','z_coords')/1000.
    xs = np.arange(var1.shape[1])*5
    m = np.argmin(np.abs(height-5))
    var1[:m,:]=np.min(var1[m:,:])
    var2[:m,:]=np.min(var2[m:,:])
    plt.subplot(1,2,1)
    plt.contourf(xs,height,var1,levels=np.linspace(var1.min(),var1.max(),20))
    plt.title('0-2 km')
    plt.xlabel(str(rh0))
    plt.ylabel('Height (km)')
    plt.ylim(5,18)
    plt.colorbar()
    plt.subplot(1,2,2)
    plt.contourf(xs,height,var2,levels=np.linspace(var2.min(),var2.max(),20))
    plt.title('2-4 km')
    plt.xlabel(str(rh1))
    plt.yticks([])
    plt.ylim(5,18)                  
    plt.colorbar() 
    plt.suptitle(xdir)
    plt.savefig('surfacetracers2panel-'+xdir+'.png')
    plt.clf()


def plot2d(xdir,varname,var):
    height = getvar('/nobackup/rstorer/convperts/revu/'+xdir+'/'+xdir+'-revu-001.h5','z_coords')/1000.
    xs = np.arange(var.shape[1])*5
    m = np.argmin(np.abs(height-5))
    var[:m,:]=np.min(var[m:,:])
    plt.contourf(xs,height,var,levels=np.linspace(var.min(),var.max(),20))
    plt.title(xdir)
    plt.xlabel('Time (min)')
    plt.ylabel('Height (km)')
    plt.ylim(5,18)
    plt.colorbar()
    plt.savefig('total2dprof-'+xdir+'-'+varname+'.png')
    plt.clf()

def getprofs(xdir,varname):
    files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/'+xdir+'/trac*h5'))
    nt = len(files)
    varout = np.zeros((82,nt))
    for i,fil in enumerate(files):
        t = getvar(fil,varname)*100*100*100
        p = np.sum(np.sum(t,1),1)
        varout[:,i]=p
    return varout


modeldirs = pert75()
varnames = ['tracer002','tracer003','tracer004','tracer005','tracer006']

#for varname in varnames:
#    saveout = {}
#    for xdir in modeldirs:
#        print xdir, varname
#        v = getprofs(xdir,varname)
#        plot2d(xdir,varname,v)
#        saveout[xdir] = v
#    np.savez('total2dprof-'+varname+'.npz',**saveout)

for varname in varnames:
    vall = np.load('total2dprof-'+varname+'.npz')
    for xdir in modeldirs:
        v = vall[xdir]
        y = np.zeros_like(v)
        for a in range(v.shape[1]):
            y[:,a] = v[:,a] - v[:,0]
        plot2d(xdir,varname+'-diff-upper',y)


vallsfc = np.load('total2dprof-tracer002.npz')
vall24 = np.load('total2dprof-tracer003.npz')
#vall46 = np.load('total2dprof-tracer004.npz')
#vall68 = np.load('total2dprof-tracer005.npz')
#vall10 = np.load('total2dprof-tracer006.npz')

rh0 = np.load('rh-z-0-2000.npz')
rh1 = np.load('rh-z-2000-4000.npz')

for xdir in modeldirs:
    v1 = vallsfc[xdir]
    v2 = vall24[xdir]
#    v3 = vall46[xdir]
#    v4 = vall68[xdir]
#    v5 = vall10[xdir]
    y1 = np.zeros_like(v1)
    y2 = np.zeros_like(v2)
#    y3 = np.zeros_like(v3)
#    y4 = np.zeros_like(v4)
#    y5 = np.zeros_like(v5)
    for a in range(v1.shape[1]):
        y1[:,a] = v1[:,a] - v1[:,0]
        y2[:,a] = v2[:,a] - v2[:,0]
#        y3[:,a] = v3[:,a] - v3[:,0]
#        y4[:,a] = v4[:,a] - v4[:,0]
#        y5[:,a] = v5[:,a] - v5[:,0]
    plot2d2panel(xdir,y1,y2,rh0[xdir],rh1[xdir])
#    plot2d5panel(xdir,y1,y2,y3,y4,y5)











