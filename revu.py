'''The REVUIN file should be setup to go for the first timestep, just edit number of times and filename'''
import os
import glob

def runrevu(filename, numfiles):
    tprev = '001'
    tcurr = str(numfiles)
    t=1
    print numfiles
    for t in range(1,numfiles):
        runcommand = '/nobackup/rstorer/code/revu-6.2.01 -f '+filename
        print t, runcommand
        print tcurr
        os.system(runcommand)

        tprev = str(t)
        tcurr = str(t+1)
        curr = t+1

        numcomm = 'sed -i.bak s/'+tprev+':'+tprev+':1/'+tcurr+':'+ tcurr + ':1/g ' + filename
        print numcomm
        os.system(numcomm)

        if curr < 100:
            tcurr = '0' + tcurr
        if curr < 10:
            tcurr = '0' + tcurr
        if t < 100:
            tprev = '0' + tprev
        if t < 10:
            tprev = '0' + tprev

        namecomm = 'sed -i.bak s/basic'+tprev+'/basic'+tcurr+'/g ' + filename
        print namecomm
        os.system(namecomm)
    print t
    namecomm = 'sed -i.bak s/basic'+tcurr+'/basic'+'001'+'/g ' + filename
    print namecomm
    os.system(namecomm)
    numcomm = 'sed -i.bak s/'+str(t+1)+':'+str(t+1)+':1/1:1:1/g ' + filename
    print numcomm
    os.system(numcomm)

maindir = '/nobackup/rstorer/perts'
modeldirs = os.walk(maindir).next()[1]
filename = '/nobackup/rstorer/code/REVUIN'
print modeldirs
for dirs in modeldirs:    
    print dirs
    namecomm = 'sed -i.bak s/modeldir/'+dirs+'/g ' + filename
    print namecomm
    os.system(namecomm)
    numfiles = len(glob.glob(maindir+dirs+'/out/*h5'))
    print numfiles, numfiles, numfiles, '???'
    if numfiles >0:
        runrevu(filename, numfiles)
    namecomm = 'sed -i.bak s/'+dirs+'/modeldir/g ' + filename
    print namecomm
    os.system(namecomm)
    


os.system('rm *bak')
os.system('rm sed*')

