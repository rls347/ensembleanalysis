import numpy as np
import h5py as hdf
from rachelutils.hdfload import getvar

def calc_diam(fil,varname,cname,cfmas,pwmas,unit):
    mfile = hdf.File(fil,'r')
    mass = getvar(mfile,varname)/1000.
    conc = getvar(mfile,cname[varname])
    rpw = 1./pwmas[varname]
    if varname == 'cloud' or varname == 'drizzle':
        conc = conc* 1e6

    diam=(mass/(cfmas[varname]*conc))**(1/pwmas[varname])
    diam[np.isnan(diam)] = 0.
    diam[mass<1e-10]=0
    
    label = unit[varname]
    if label == 'mm':
        diam=diam*1000.
    else:
        diam=diam*1e6
    print varname, diam[diam>0].min(), diam.max(), label
    mfile.close()

    return diam


mdir = '/nobackup/rstorer/convperts/mature/'
modeldirs = ['feb23-control']
for i in range(24):
    modeldirs.append('feb23-pert'+str(i+1))
modeldirs.append('aug17-control')
for i in range(24):
    modeldirs.append('aug17-pert'+str(i+1))
modeldirs.append('aug11-control')
for i in range(24):
    modeldirs.append('aug11-pert'+str(i+1))


varnames = ['cloud','rain','pristine','snow','aggregates','graupel','hail','drizzle']
shape = {'cloud':0.5,'drizzle':0.5,'rain':0.5,'pristine':0.179,'snow':0.179,'aggregates':0.5,'graupel':0.5,'hail':0.5}
cfmas = {'cloud':524.,'drizzle':524.,'rain':524.,'pristine':110.8,'snow':2.739e-3,'aggregates':.496,'graupel':157.,'hail':471.}
pwmas = {'cloud':3.,'drizzle':3.,'rain':3.,'pristine':2.91,'snow':1.74,'aggregates':2.4,'graupel':3.,'hail':3.}
cname = {'cloud':'cloud_concen_mg','drizzle':'drizzle_concen_mg','rain':'rain_concen_kg','pristine':'pris_concen_kg',
        'snow':'snow_concen_kg','aggregates':'agg_concen_kg','graupel':'graup_concen_kg','hail':'hail_concen_kg'}
mult = {'cloud':6,'rain':3,'pristine':6,'snow':3,'aggregates':3,'graupel':3,'hail':3,'drizzle':6}
outlabel = {'cloud':'microns','rain':'mm','pristine':'microns','snow':'mm','aggregates':'mm','graupel':'mm','hail':'mm','drizzle':'microns'}

dfil = '/nobackup/rstorer/convperts/mature-orig/aug11-control/revu/testdiams-out--AS-1999-01-26-120000-g1.h5'

#dcalc=calc_diam(mdir+'/aug11-control/aug11-control-mature-001.h5','cloud',cname,cfmas,pwmas,outlabel)
cdiam = getvar(dfil,'cloud_diam')
print 'cloud', cdiam[cdiam>0].min(), cdiam.max()
cic = np.where(cdiam>40.4)
cib = np.where(np.logical_and(cdiam<1.98,cdiam> 0.0))
cil = np.where(cdiam>0.0)
print 'large: ', 100*(1.0*len(cic[0]))/len(cil[0])
print 'small: ', 100*(1.0*len(cib[0]))/len(cil[0])
print ' '
rdiam = getvar(dfil,'rain_diam')
print 'rain', rdiam[rdiam>0].min(), rdiam.max()
ric = np.where(rdiam>5.05)
rib = np.where(np.logical_and(rdiam<0.297,rdiam>0.0))
ril = np.where(rdiam>0.0)
print 'large: ', 100*(1.0*len(ric[0]))/len(ril[0])
print 'small: ', 100*(1.0*len(rib[0]))/len(ril[0])
print ' '
pdiam = getvar(dfil,'pris_diam')
print 'pristine', pdiam[pdiam>0].min(), pdiam.max()
pic = np.where(pdiam>126.25)
pib = np.where(np.logical_and(pdiam<14.85,pdiam>0.0))
pil = np.where(pdiam>0.0)
print 'large: ', 100*(1.0*len(pic[0]))/len(pil[0])
print 'small: ', 100*(1.0*len(pib[0]))/len(pil[0])
print ' '
sdiam = getvar(dfil,'snow_diam')
print 'snow', sdiam[sdiam>0].min(), sdiam.max()
sic = np.where(sdiam>10.1)
sib = np.where(np.logical_and(sdiam<.099,sdiam>0.0))
sil = np.where(sdiam>0.0)
print 'large: ', 100*(1.0*len(sic[0]))/len(sil[0])
print 'small: ', 100*(1.0*len(sib[0]))/len(sil[0])
print ' '
adiam = getvar(dfil,'agg_diam')
print 'agg', adiam[adiam>0].min(), adiam.max()
aic = np.where(adiam>10.1)
aib = np.where(np.logical_and(adiam<.298,adiam>0.0))
ail = np.where(adiam>0.0)
print 'large: ',100*(1.0*len(aic[0]))/len(ail[0])
print 'small: ', 100*(1.0*len(aib[0]))/len(ail[0])
print ' '
gdiam = getvar(dfil,'graup_diam')
print 'graupel', gdiam[gdiam>0].min(), gdiam.max()
gic = np.where(gdiam>5.05)
gib = np.where(np.logical_and(gdiam<.297,gdiam>0.0))
gil = np.where(gdiam>0.0)
print 'large: ',100*(1.0*len(gic[0]))/len(gil[0])
print 'small: ', 100*(1.0*len(gib[0]))/len(gil[0])
print ' '
hdiam = getvar(dfil,'hail_diam')
print 'hail', hdiam[hdiam>0].min(), hdiam.max()
hic = np.where(hdiam>10.1)
hib = np.where(np.logical_and(hdiam<.792,hdiam>0.0))
hil = np.where(hdiam>0.0)
print 'large: ',100*(1.0*len(hic[0]))/len(hil[0])
print 'small: ', 100*(1.0*len(hib[0]))/len(hil[0])
print ' '
ddiam = getvar(dfil,'drizzle_diam')
print 'drizzle', ddiam[ddiam>0].min(), ddiam.max()
dic = np.where(ddiam>101.0)
dib = np.where(np.logical_and(ddiam<64.35,ddiam>0.0))
dil = np.where(ddiam>0.0)
print 'large: ',100*(1.0*len(dic[0]))/len(dil[0])
print 'small: ', 100*(1.0*len(dib[0]))/len(dil[0])
print ' '
