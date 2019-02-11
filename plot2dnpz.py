import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def movie2d(varname):
	filename = '/nobackup/rstorer/filesnpz/mature'+varname+'.npz'
	varall = np.load(filename)
	test = ['feb23-control','aug11-control','aug17-control']
	for xdir in test:#varall.keys():
		print varname, xdir
		var = varall[xdir]
		nt,ny,nx = var.shape
		xs = np.arange(nx)*(100./nx)
		ys = xs
		levels = np.linspace(500,np.max(var),20)

		fig = plt.figure()
		z2 = var[0,:,:]
		cont2 = plt.contourf(xs,ys,z2,levels=levels)
		c2 = plt.colorbar(cont2)
		def animate(i):
			plt.clf()
			z2 = var[i,:,:]
			cont2 = plt.contourf(xs,ys,z2,levels=levels)
			plt.colorbar(cont2)
			title='Time ' + str(i)
			plt.title(title)
			return cont2
		anim = animation.FuncAnimation(fig, animate, frames=nt)
		anim.save('/nobackup/rstorer/plots/'+xdir+varname+'TESTmature.mp4')



movie2d('cloudtops')
#movie2d('columnmaxw')
#movie2d('cloudtopw')


