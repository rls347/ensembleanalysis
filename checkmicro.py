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
case = 'aug11'
xdir = 'control'
allvars = {}
filesrams = sorted(glob.glob(maindir+case+'-'+xdir+"/revu/*h5"))
numfiles = len(filesrams)

fil = hdf.File(filesrams[-1], 'r')
for varname in varlist:
	slicevar = np.squeeze(fil[varname].value[:,:,160:170,:])
	tmp = np.mean(slicevar,1)
	allvars[varname] = tmp[:,300]
height = np.squeeze(fil['z_coords'].value)
lvvap = 2.5e6/(1000.*1004)
lvfrz = .334e6/(1000.*1004)
lvboth = 2.8334e6/(1000.*1004)

totmelt = allvars['meltprist']+allvars['meltsnowt']+allvars['meltaggrt']+allvars['meltgraut']+allvars['melthailt']
diff = totmelt - allvars['melticet']
print 'melt', diff, totmelt

totvapl = allvars['vapcldt']+allvars['vapraint']+allvars['vapdrizt']
diff = totvapl - allvars['vapliqt']
print 'vapliq',diff, totvapl

totvapi = allvars['vapprist']+allvars['vapsnowt']+allvars['vapaggrt']+allvars['vapgraut']+allvars['vaphailt']
diff = totvapi - allvars['vapicet']
print 'vapice',diff, totvapi

totrime = allvars['rimecldsnowt']+allvars['rimecldaggrt']+allvars['rimecldgraut']+allvars['rimecldhailt']
diff = totrime - allvars['rimecldt']
print 'rime',diff, totrime
print ' '
print ' '
print totmelt*lvfrz
print totvapi*lvboth
print totvapl*lvvap
print totrime*lvfrz
print allvars['latheatfrzt']+allvars['latheatvapt']

plt.plot(allvars['nucicert']*lvfrz,height,label = 'icenuc', linewidth = 3)
plt.plot(allvars['nuccldrt']*lvvap,height,label = 'nucliq', linewidth = 3)
plt.plot(totmelt*lvfrz,height,label = 'melt', linewidth = 3)
plt.plot(totvapi*lvboth,height,label = 'vapice', linewidth = 3)
plt.plot(totvapl*lvvap,height,label = 'vapliq', linewidth = 3)
plt.plot(totrime*lvfrz,height,label = 'rime', linewidth = 3)
plt.plot(allvars['rain2icet']*lvfrz,height,label = 'rain2ice', linewidth=3)
plt.plot(allvars['latheatfrzt'],height,label = 'latentfrz', linewidth = 3)
plt.plot(allvars['latheatvapt'],height,label = 'latentvap', linewidth = 3)
plt.plot((totmelt*lvfrz+allvars['rain2icet']*lvfrz+totvapi*lvboth+totvapl*lvvap+totrime*lvfrz+allvars['nucicert']*lvfrz+allvars['nuccldrt']*lvvap), height,label = 'sum', linewidth = 3)
plt.legend()
plt.savefig('../plots/microcheckprofs.png')
plt.clf()

varlist2 = ['nuccldrt','cld2raint','ice2raint','nucicert','vapliqt','vapicet','melticet',
		'rimecldt','rain2icet','aggregatet','inuchomrt','inuccontrt','inucifnrt','inuchazrt',
		'vapcldt','vapraint','vapprist','vapsnowt','vapaggrt','vapgraut','vaphailt','vapdrizt',
		'meltprist','meltsnowt','meltaggrt','meltgraut','melthailt','rimecldsnowt','rimecldaggrt',
		'rimecldgraut','rimecldhailt','rain2prt','rain2agt','rain2grt','rain2hat','rain2snt']

for varname in varlist2:
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofilesall.png')
plt.clf()

varlist2 = ['nuccldrt','cld2raint','ice2raint','nucicert','vapliqt','vapicet','melticet']
for varname in varlist2:
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofiles1.png')
plt.clf()

varlist2 = ['rimecldt','rain2icet','aggregatet','inuchomrt','inuccontrt','inucifnrt','inuchazrt']
for varname in varlist2:        
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofiles2.png')
plt.clf()

varlist2 = ['vapcldt','vapraint','vapprist','vapsnowt','vapaggrt','vapgraut','vaphailt','vapdrizt']
for varname in varlist2:
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofiles3.png')
plt.clf()

varlist2 = ['meltprist','meltsnowt','meltaggrt','meltgraut','melthailt','rimecldsnowt','rimecldaggrt']
for varname in varlist2:
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofiles4.png')
plt.clf()

varlist2 = ['rimecldgraut','rimecldhailt','rain2prt','rain2agt','rain2grt','rain2hat','rain2snt']
for varname in varlist2:
	plt.plot(allvars[varname],height,label = varname, linewidth=2)
plt.legend()
plt.savefig('../plots/microprofiles5.png')
plt.clf()





















