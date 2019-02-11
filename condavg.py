import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation

'''Creates an XZ slice of averaged condensate for each time, then makes a movie'''

maindir = '/nobackup/rstorer/convperts/revu/'
modeldirs = os.walk(maindir).next()[1]
modeldirs = ['aug11-control','aug17-control','feb23-control']
xs = np.arange(400)*(100./400.)
#levels = np.logspace(-3,1,20)  #log cond
levels = np.linspace(0.01,3,20) #avg cond
#levels=np.logspace(-2,1.3,20)

#levels = np.linspace(0,60,20)  #w
for xdir in modeldirs:
    print xdir 
    filesrams = sorted(glob.glob(maindir+xdir+"/*h5"))
    numfiles = len(filesrams)
    for i in range(numfiles):
        fil = hdf.File(filesrams[i], 'r')
        pcp=np.mean(np.squeeze(fil['total_cond'].value),1)
        height = np.squeeze(fil['z_coords'].value)
         
        outi = str(i*5)
        if i*5 < 10:
            outi = '0' + outi
        if i*5 < 100:
            outi = '0' + outi
#These values are for 30s output
#			if i < 4:
#				outi = '0'+outi
#			if i < 33:
#				outi = '0'+outi 
#			if i < 333:
#				outi = '0'+outi
#			if i < 3333:
#				outi = '0'+outi
        try:
            fig = plt.figure()
            pcp[pcp<0.0001]=np.log(0)
            f = plt.contourf(xs, height, pcp, levels = levels)
            if height.max() > 20000:
                plt.ylim(0,17000)
            if height.max() < 50:
                plt.ylim(0,17)
            if xdir == 'aug11-control':
                nam = 'Aug 11 '
            if xdir == 'aug17-control':
                nam = 'Aug 17 '
            if xdir == 'feb23-control':
                nam = 'Feb 23 '

	        cbar = plt.colorbar(f)
            plt.title(nam+'Avg Condensate '+str(i*5) + ' min', size = 20)
            plt.savefig('../plots/newavgcond'+xdir+outi+'.png')
            plt.close()
        except:
            print 'nothing to plot in ', i, outi, pcp.max(), pcp.min()
			
#		os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/newmaxw"+xdir+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/newmaxw"+xdir+".mp4")
#		os.system("rm ../plots/newmaxw"+xdir+"*.png")
    os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/newavgcond"+xdir+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/newavgcond"+xdir+".mp4")
    os.system("rm ../plots/newavgcond"+xdir+"*.png")

