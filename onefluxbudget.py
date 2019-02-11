import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py as hdf
from rachelutils.hdfload import getvar
import glob
from rachelutils.hdfload import getdz

def getbudgetvars(fil1,fil2,dt):
    cond1 = getvar(fil1, 'total_cond')/1000.
    cond2 = getvar(fil2, 'total_cond')/1000.
    rho1 = (getvar(fil1, 'press') * 100.) / (getvar(fil1, 'tempk') *287.)
    rho2 = (getvar(fil2, 'press') * 100.) / (getvar(fil2, 'tempk') *287.)
    w = getvar(fil1, 'w')
    u = getvar(fil1,'u')
    v = getvar(fil1,'v')
    micro2 = (getvar(fil2, 'nuccldrt') + getvar(fil2, 'nucicert') + getvar(fil2, 'vapliqt') + getvar(fil2, 'vapicet')) / 1000.
    pcp3d = getvar(fil1,'precip3d')
    z = getvar(fil1,'z_coords')
    dz = getdz(fil1)

    diff = ((cond2*rho2*dz[:,None,None])-(cond1*rho1*dz[:,None,None]))/dt
    mic = (micro2*rho2*dz[:,None,None])/dt

    dzdz = np.zeros_like(w)
    dzdz[1:-1,:,:] = (cond1[2:,:,:]*rho1[2:,:,:]*w[2:,:,:])-(cond1[:-2,:,:]*rho1[:-2,:,:]*w[:-2,:,:])

    dzdx = np.zeros_like(u)
    dzdx[:,:,1:-1] = (cond1[:,:,2:]*rho1[:,:,2:]*u[:,:,2:])-(cond1[:,:,:-2]*rho1[:,:,:-2]*u[:,:,:-2])

    dzdy = np.zeros_like(v)
    dzdy[:,1:-1,:] = (cond1[:,2:,:]*rho1[:,2:,:]*v[:,2:,:])-(cond1[:,:-2,:]*rho1[:,:-2,:]*v[:,:-2,:])

    term = np.zeros_like(w)
    term[1:-1,:,:] = (pcp3d[2:,:,:]-pcp3d[:-2,:,:])

    vert = dzdz*-1
    horiz = (dzdx + dzdy) * -1

    rhs = mic + horiz + vert + term
    res = diff-rhs

    return w,diff,horiz,vert,term,mic,res

def makeplots(fil1,fil2,dt):
    w,diff,horiz,vert,term,micro,res = getbudgetvars(fil1,fil2,dt)
    colmax = np.max(w,0)
    w1 = np.where(colmax>1)
    ys = np.arange(400)*.25
    levs = np.linspace(-5,5,151)*1e-2
    print levs

    height = getvar(fil1,'z_coords')
    z12 = np.argmin(np.abs(height-10000))
    fig = plt.figure()
    plt.subplot(2,3,1)
    plt.contourf(ys[160:320],ys[80:240],diff[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(diff[z12,80:240,160:320]),np.min(diff[z12,80:240,160:320])
    plt.axis('scaled')
    plt.title('dq/dt')
#    plt.colorbar()
    ax = plt.gca()
    ax.set_yticks(ax.get_yticks()[::2])
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='off')

    plt.subplot(2,3,2)
    plt.contourf(ys[160:320],ys[80:240],horiz[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(horiz[z12,80:240,160:320]),np.min(horiz[z12,80:240,160:320])
    plt.axis('scaled')
#    plt.colorbar()
    plt.title('horiz adv')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(2,3,3)
    plt.contourf(ys[160:320],ys[80:240],vert[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(vert[z12,80:240,160:320]),np.min(vert[z12,80:240,160:320])
    plt.axis('scaled')
    #plt.colorbar()
    plt.title('vert adv')
    plt.xticks([])
    plt.yticks([])
    
    plt.subplot(2,3,4)
    plt.contourf(ys[160:320],ys[80:240],term[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(term[z12,80:240,160:320]),np.min(term[z12,80:240,160:320])
    plt.axis('scaled')
   # plt.colorbar()
    plt.title('vt term')
    ax = plt.gca()
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_yticks(ax.get_yticks()[::2])
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
    
    plt.subplot(2,3,5)
    plt.contourf(ys[160:320],ys[80:240],micro[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(micro[z12,80:240,160:320]),np.min(micro[z12,80:240,160:320])
    plt.axis('scaled')
    #plt.colorbar()
    plt.title('micro')
    ax = plt.gca()
    ax.set_xticks(ax.get_xticks()[::2])
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')

    fig2 = plt.subplot(2,3,6)
    fig2.contourf(ys[160:320],ys[80:240],res[z12,80:240,160:320],levels=levs,cmap=plt.get_cmap('bwr'))
    print np.max(res[z12,80:240,160:320]),np.min(res[z12,80:240,160:320])
    plt.axis('scaled')
   # plt.colorbar()
    plt.title('residual')
    ax = plt.gca()
    ax.set_xticks(ax.get_xticks()[::2])
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')

    plt.tight_layout()
    fig.subplots_adjust(right =.75)
    ax3 = fig.add_axes([0.8, 0.15, 0.03, 0.7])
    norm = matplotlib.colors.Normalize(vmin = levs.min(), vmax = levs.max())
    cb1 = matplotlib.colorbar.ColorbarBase(ax3, cmap=plt.get_cmap('bwr'),norm=norm,orientation='vertical')
    cb1.formatter.set_powerlimits((0,0))
    cb1.update_ticks()
    plt.savefig('budget10km-flux.png')
    plt.clf()
    plt.close()
    
    
    
    updraft = np.mean(vert[:,w1[0],w1[1]],1)
    vt = np.mean(term[:,w1[0],w1[1]],1) 
    dcdt = np.mean(diff[:,w1[0],w1[1]],1) 
    mic = np.mean(micro[:,w1[0],w1[1]],1) 
    hor = np.mean(horiz[:,w1[0],w1[1]],1) 
    ext = np.mean(res[:,w1[0],w1[1]],1) 

#    updraft = np.zeros_like(height)
#    vt = np.zeros_like(height)
#    dcdt = np.zeros_like(height)
#    mic = np.zeros_like(height)
#    hor = np.zeros_like(height)
#    ext = np.zeros_like(height)
#
#    for ix in range(2,80):
#        ww =np.squeeze(w[ix,:,:])
#        ww1 = np.where(ww>1)
#        updraft[ix]=np.mean(vert[ix,ww1[0],ww1[1]])
#        vt[ix]=np.mean(term[ix,ww1[0],ww1[1]])
#        dcdt[ix]=np.mean(diff[ix,ww1[0],ww1[1]])
#        mic[ix]=np.mean(micro[ix,ww1[0],ww1[1]])
#        hor[ix]=np.mean(horiz[ix,ww1[0],ww1[1]])
#        ext[ix]=np.mean(res[ix,ww1[0],ww1[1]])
#

    fig = plt.figure()
    plt.plot(dcdt[2:],height[2:],color = 'black',linewidth=2,label = 'dq/dt')
    plt.plot(hor[2:],height[2:],color = 'red', linewidth = 2, label = 'horiz adv')
    plt.plot(updraft[2:],height[2:],color='green',linewidth=2,label = 'vert adv')
    plt.plot(vt[2:],height[2:],color = 'gold', linewidth=2,label = 'vt term')
    plt.plot(mic[2:],height[2:],color = 'blue',linewidth = 2, label = 'micro')
    plt.plot(ext[2:],height[2:],color = 'gray', linewidth = 2, label = 'residual')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel('kg/kg/s')
    plt.ylabel('z (m)')
    plt.ylim(0,18000)
#    plt.xlim(-1e-6,1e-6)
    plt.legend()
    plt.savefig('budget-profsw1-flux.png')
    plt.clf()



files = sorted(glob.glob('/nobackup/rstorer/convperts/revu/aug11-control/*h5'))
outdir = '/nobackup/rstorer/plots/'

num= 25
makeplots(files[num],files[num+1],300.)






