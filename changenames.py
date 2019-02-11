import glob
import numpy as np
import os

cases = ['aug11','aug17','feb23']
modeldirs = []
for case in cases:
    modeldirs.append(case+'-control')
    for i in range(1,25):
        modeldirs.append(case+'-pert'+str(i))

maindir = '/nobackup/rstorer/convperts/'
chunks = ['revu','growing','mature']

chunks = ['revu']
modeldirs = ['aug11-pert8','aug11-pert9']

for chunk in chunks:
	for dir in modeldirs:
		filedir = maindir+chunk+'/'+dir
		files = sorted(glob.glob(filedir+'/basic*out*h5'))
		print filedir, len(files)
		for t in range(len(files)):
			tcurr = str(t+1)
			if t < 99:
				tcurr = '0' + tcurr
			if t < 9:
				tcurr = '0' + tcurr
			oldname = filedir+'/basic'+tcurr+'-out--AS-1999-01-26-120000-g1.h5'
			newname = filedir+'/'+dir+'-'+chunk+'-'+tcurr+'.h5'
			cmd = 'mv '+oldname+' '+newname
			os.system(cmd)
