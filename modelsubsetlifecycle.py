import numpy as np
import h5py as hdf
import glob
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


filename = '/nobackup/rstorer/filesnpz/cloudtops.npz'
varall = np.load(filename)
filnam = '/nobackup/rstorer/filesnpz/revucolumnmaxw.npz'
maxws = np.load(filnam)

cases = ['aug11','aug17','feb23']
modeldirs = []
for case in cases:
	modeldirs.append(case+'-control')
	for i in range(1,25):
		modeldirs.append(case+'-pert'+str(i))

for xdir in modeldirs:
    var = varall[xdir]
    w = maxws[xdir]
    nt,ny,nx = var.shape
    maxt = np.max(np.max(var,1),1)
    maxw = np.max(np.max(w,1),1)
    t5 = nt *5
    t10 = nt *5
    t8 = nt *5
    t12 = nt *5

    for i in range(nt-1,0,-1):
        if maxt[i] > 5000:
            t5=i *5
        if maxt[i] > 8000:
            t8=i *5
        if maxt[i] > 10000:
            t10 = i *5
        if maxt[i] > 12000:
            t12 = i *5

    if xdir[0:5] == 'aug17':
        convoff = 60
    else:
        convoff = 180

    tt = np.argmax(maxt) *5
    ww = np.argmax(maxw) *5
    stt = np.min([tt,ww])
    if stt<(t5+25):
        ts = t5+25
    else:
        ts = stt

    if ww < (ts+30):
        tstr = ts+30
    else:
        tstr = ww

    timestrat = '{:02d}{:02d}'.format(*divmod((tstr)+720,60))
    timegrow = '{:02d}{:02d}'.format(*divmod((t5-5)+720,60))
    timemat = '{:02d}{:02d}'.format(*divmod((ts)+720,60))
    filenameold = 'out--A-1999-01-26-'+timegrow+'00-head.txt'
    filenamenew = 'out--A-1999-01-26-'+timemat+'00-head.txt'
    filenamelast = 'out--A-1999-01-26-'+timestrat+'00-head.txt'
	#filename = '\/nobackup\/rstorer\/convperts\/'+xdir+'\/out--A-1999-01-26-'+time0+'00-head.txt'
#	print filename
    endtime = str((tstr+30)*60)
    copystartfile = 'scp /u/rstorer/convperts/'+xdir+'/out--A-1999-01-26-'+timestrat+'* /nobackup/rstorer/convperts/'+xdir+'/'
    changeHFILIN = "sed -i 's/"+filenamenew+"/"+filenamelast+"/g' /nobackup/rstorer/convperts/ramsinfiles/ramsin-"+xdir
    changeendtime= "sed -i 's/   TIMMAX   = /   TIMMAX   =  "+endtime+"., !/g' /nobackup/rstorer/convperts/ramsinfiles/ramsin-"+xdir
    cmd = "sed -n '187p' " + "/nobackup/rstorer/convperts/ramsinfiles/ramsin-"+xdir  #This prints line 187 to screen
    print timestrat, endtime
    os.system(cmd)
    cmd2 = "sed -n '20p' " + "/nobackup/rstorer/convperts/ramsinfiles/ramsin-"+xdir 
    os.system(cmd2)
    print ' ' 
	
	



	

		

