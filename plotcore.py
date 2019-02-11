import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def movie2d(varname):
	filename = '/nobackup/rstorer/filesnpz/'+varname+'.npz'
	varall = np.load(filename)
	for xdir in varall.keys():
		print varname, xdir
		var = varall[xdir]
		nt,ny,nx = var.shape
		xs = np.arange(nx)*(100./nx)
		ys = xs
		levels = np.linspace(0,np.max(var),20)

		fig = plt.figure()
		z2 = var[0,:,:]
		cont2 = plt.contourf(xs,ys,z2,levels=levels)
		c2 = plt.colorbar(cont2)
		def animate(i):
			z2 = var[i,:,:]
			cont2 = plt.contourf(xs,ys,z2,levels=levels)
			title='Time ' + str(i)
			plt.clf()
			return cont2
		anim = animation.FuncAnimation(fig, animate, frames=nt)
		anim.save('/nobackup/rstorer/plots/'+xdir+varname+'.mp4')



movie2d('cloudtops')
movie2d('columnmaxw')
movie2d('cloudtopw')


