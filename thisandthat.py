import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

def getvar(filename, names):
	wholevar = np.load(filename)
	newvar = np.zeros(75)
	for i in range(75):
		newvar[i] = wholevar[names[i]]
	return newvar

def splitcase(filename, cases, perts):
	wholevar = np.load(filename)
	var1 = np.zeros(25)
	var2 = np.zeros(25)
	var3 = np.zeros(25)
	for i in range(25):
		name = cases[0]+perts[i]
		var1[i] = wholevar[name]
		name = cases[1]+perts[i]
		var2[i] = wholevar[name]
		name = cases[2]+perts[i]
		var3[i] = wholevar[name]
	return var1, var2, var3

	

cases = ['aug17','aug11','feb23']
perts = ['-control']
for i in range(1,25):
	perts.append('-pert'+str(i))
names = []
for case in cases:
	for i in range(25):
		names.append(case+perts[i])

files = sorted(glob.glob('../filesnpz/*npz'))
nvar = len(files)
listofvars = []
#for filename in files:
#	listofvars.append(getvar(filename, names))
xvars = ['cape_ML','rhlow','maxwpoints','totpcpmm','convprecipfrac']
yvars = ['maxwpoints','convprecipmm','totpcpmm','convprecipfrac','revumaxwavgoftime', 'revuechotop0avgoftime','revuintabove10kmiceavgoftime','revuintabove5kmcondavgoftime',
		'revuintabove5kmtracer2avgoftime','revuintabove8kmliquidavgoftime','revuintlatentavgoftime','revumaxwabove5kmavgoftime', 'revuechotop10avgoftime',
		'revuintabove10kmlatentavgoftime','revuintabove5kmiceavgoftime','revuintabove8kmcondavgoftime','revuintabove8kmtracer2avgoftime', 
		'revuintliquidavgoftime','revuminwavgoftime','revuechotop5avgoftime','revuintabove10kmliquidavgoftime',  'revuintabove5kmlatentavgoftime', 
		'revuintabove8kmiceavgoftime','revuintcondavgoftime','revuinttracer2avgoftime','revuminwabove5kmavgoftime', 'revuintabove10kmcondavgoftime', 
		'revuintabove10kmtracer2avgoftime', 'revuintabove5kmliquidavgoftime', 'revuintabove8kmlatentavgoftime', 'revuinticeavgoftime',
		'revumaxwmaxoftime', 'revuechotop0maxoftime','revuintabove10kmicemaxoftime','revuintabove5kmcondmaxoftime', 'revuintabove5kmtracer2maxoftime', 
		'revuintabove8kmliquidmaxoftime',  'revuintlatentmaxoftime', 'revumaxwabove5kmmaxoftime', 'revuechotop10maxoftime', 'revuintabove10kmlatentmaxoftime',  
		'revuintabove5kmicemaxoftime','revuintabove8kmcondmaxoftime','revuintabove8kmtracer2maxoftime', 'revuintliquidmaxoftime','revuminwmaxoftime', 
		'revuechotop5maxoftime','revuintabove10kmliquidmaxoftime',  'revuintabove5kmlatentmaxoftime', 'revuintabove8kmicemaxoftime','revuintcondmaxoftime', 
		'revuinttracer2maxoftime','revuminwabove5kmmaxoftime', 'revuintabove10kmcondmaxoftime', 'revuintabove10kmtracer2maxoftime', 
		'revuintabove5kmliquidmaxoftime', 'revuintabove8kmlatentmaxoftime',  'revuinticemaxoftime']
yvars = ['maxwpoints']
xvars = ['cape_ML']
#for i in range(nvar-1):
#	xvar = listofvars[i]
#	for j in range(i,nvar):
#		yvar = listofvars[j]
#		plt.scatter(xvar,yvar)
#		plt.ylabel(files[j])
#		plt.xlabel(files[i])
#		title = 'var'+str(i)+'_var'+str(j)
#		plt.title(title)
#		plt.savefig('../plots/scatterplots/'+title+'scatter.png')
#		plt.clf()

#for yvar in yvars:
#	x = getvar('../filesnpz/rhlow.npz',names)
#	y = getvar('../filesnpz/cape.npz',names)
#	z = getvar('../filesnpz/'+yvar+'.npz',names)
#	print yvar, z
#	plt.scatter(x,y,c=z)
#	plt.xlabel('Low Level RH')
#	plt.ylabel('Cape')
#	plt.title(yvar)
#	plt.colorbar()
#	plt.savefig('../plots/scatterplots/'+yvar+'-3dscattermap.png')
#	plt.clf()
#yvars = ['maxwpoints']
#xvars = ['rhlow']

#xvars = ['ltss','rhlow','rhmid','rhhigh','cape_ML','maxwpoints']
#yvars = ['ltss','rhlow','rhmid','rhhigh','cape_ML','maxwpoints','totpcpmm','maturediamcloud','maturediamrain',
#		'maturediampristine','maturediamsnow','maturediamdrizzle','maturediamgraupel',
#		'maturediamaggregates','maturediamhail']

for xvar in xvars:
	for yvar in  yvars:
		x = getvar('../filesnpz/'+xvar+'.npz',names)
		y = getvar('../filesnpz/'+yvar+'.npz',names)#*1000.
		plt.scatter(x**.5,y)
        plt.plot(x**.5,x**.5,color='black',linestyle='dashed')
        plt.plot(x**.5,(.5*(x**.5)),color='black',linestyle='dotted')
        plt.ylabel('Max W')
        plt.xlabel('sqrt(CAPE)')
		#plt.title(xvar+' vs ' +yvar)
        plt.savefig('sqrt'+xvar+'_'+yvar+'scatter.png')#('../plots/massfluxplots/'+xvar+'_'+yvar+'scatter.png')
        plt.clf()
        y2 = np.arange(40)
        xa17,xa11,xf23 = splitcase('../filesnpz/'+xvar+'.npz', cases, perts)
        ya17,ya11,yf23 = splitcase('../filesnpz/'+yvar+'.npz', cases, perts)
#        plt.scatter(xa17**.5,ya17,color = 'c',label = 'Aug 17', s=50)
        fig = plt.figure(figsize=(8,8))
        plot = fig.add_subplot(111)

# We change the fontsize of minor ticks label 
        plot.tick_params(axis='both', which='major', labelsize=20)
        plot.tick_params(axis='both', which='minor', labelsize=20)
        plt.scatter(.5*(xa11**.5),ya11,color = 'b',label = 'Aug 11', s=50)
        plt.scatter(.5*(xf23**.5),yf23,color = 'b',label = 'Feb 23', s=50)
#        plt.plot(x**.5,x**.5,color='black',linestyle='dashed')
        plt.plot(y2,y2,'--k')
#        plt.legend(loc='upper left')
        plt.xlabel('1/2 '+r'$\mathbf{\sqrt{CAPE}}$'+'    (m/s)',size=22,fontweight='normal')
        plt.ylabel('Max W (m/s)',size=22,fontweight='normal')
        plt.xlim(5,35)
        plt.ylim(5,60)
        plt.title('CAPE vs Vertical Velocity',size=24,fontweight='normal')
        plt.savefig('sqrt'+xvar+'_'+yvar+'split.png',dpi=300)#('../plots/massfluxplots/'+xvar+'_'+yvar+'split.png')
        plt.clf()

