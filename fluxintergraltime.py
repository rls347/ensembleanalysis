import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rachelutils.dumbnaming import pert75

modeldirs = pert75()

cond = np.load('budget-timeseries-updraftcondflux.npz')
vapor = np.load('budget-timeseries-updraftvaporflux.npz')
tracer = np.load('budget-timeseries-updrafttracer2flux.npz')
rh = np.load('../filesnpz/rhlow.npz')

#want to make time series that's colored by RH. 

condout = {}
vapout = {}
tracout = {}

for xdir in modeldirs:
    condout[xdir]=np.sum(cond[xdir])
    vapout[xdir] = np.sum(vapor[xdir])
    tracout[xdir]=np.sum(tracer[xdir])


np.savez('budget-total-updraftcondflux.npz',**condout)
np.savez('budget-total-updraftvaporflux.npz',**vapout)
np.savez('budget-total-updrafttracer2flux.npz',**tracout)


