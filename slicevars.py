import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.animation as animation


maindir = '/nobackup/rstorer/convperts/mature-orig/'
modeldirs = ['control']
#for i in range(1,25):
#    modeldirs.append('pert'+str(i))

cases = ['feb23','aug11','aug17']
case = cases[0]

#xval = [166,164,163]

#0 60
#163 243

#aug11-control
#0 60
#164 256

#feb23-control
#0 60
#166 247

varlist = ['nuccldrt','cld2raint','ice2raint','nucicert','vapliqt','vapicet','melticet',
		'rimecldt','rain2icet','aggregatet','inuchomrt','inuccontrt','inucifnrt','inuchazrt',
		'vapcldt','vapraint','vapprist','vapsnowt','vapaggrt','vapgraut','vaphailt',
		'vapdrizt','meltprist','meltsnowt','meltaggrt','meltgraut','melthailt','rimecldsnowt',
		'rimecldaggrt','rimecldgraut','rimecldhailt','rain2prt','rain2agt','rain2grt',
		'rain2hat','rain2snt','aggrselfprist','aggrselfsnowt','aggrprissnowt','latheatfrzt',
		'latheatvapt','cloud','rain','drizzle','hail','graupel','snow','pristine','aggregates']
for varname in varlist:
  print varname
  for case in cases:
    pcpmax = []
    pcp = {}
    for xdir in modeldirs:
        print case, xdir
        filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/revu/*h5"))
        numfiles = len(filesrams)
        print numfiles
        pcp[xdir] = []
        for i in range(numfiles):
            fil = hdf.File(filesrams[i], 'r')
            #slicevar = np.squeeze(fil['latheatvapt'].value[:,:,160:170,:])+np.squeeze(fil['latheatfrzt'].value[:,:,160:170,:])
            slicevar = np.squeeze(fil[varname].value[:,:,160:170,:])
            if i ==0:
                slicevar=slicevar*0.0
            pcp[xdir].append(np.mean(slicevar,1))
    fil2 = hdf.File('/nobackup/rstorer/convperts/mature/feb23-control/feb23-control-mature-001.h5','r')
    height = np.squeeze(fil2['z_coords'].value)
    fil2.close()
    xs = np.arange(400)*.25
    maxvar = np.max(np.asarray(pcp[xdir]))
    minvar = np.min(np.asarray(pcp[xdir]))
#    levels=np.logspace(-2,1.3,20)
    levels = np.linspace(minvar,maxvar,20)
    for i in range(numfiles):
        outi = str(i)
        if i < 10:
           outi = '0'+outi

        fig = plt.figure()
        z2 = pcp[xdir][i]
        f = plt.contourf(xs, height, z2, levels = levels)
        if height.max() > 20000:
        	plt.ylim(0,18000)
        if height.max() < 50:
        	plt.ylim(0,18)
        cbar = plt.colorbar(f)
        plt.suptitle('Latent Heat '+str(i*30) + ' s', size = 20)
        plt.savefig('../plots/latentslice/'+varname+case+outi+'.png')
        plt.close()

    os.system("ffmpeg -framerate 10 -pattern_type glob -i '../plots/latentslice/"+varname+case+"*.png' -c:v libx264 -pix_fmt yuv420p ../plots/latentslice/"+varname+case+".mp4") 
    os.system("rm ../plots/latentslice/"+varname+case+"*.png")


