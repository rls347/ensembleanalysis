import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import atmos
from rachelutils.thermo import get_cape

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
from matplotlib import gridspec
import matplotlib.image as mpimg



filename = 'KWAJEX_Soundings_11Aug1999/sounding_11aug1999_10mb_control.txt'
var = np.loadtxt(filename, dtype=float)
p = var[:,0]
T = var[:,1]
rv = var[:,2]*1000.
u = var[:,3]
v = var[:,4]


data = {'T':T+273.15, 'rv':rv/1000., 'p':p*100.}
Td = atmos.calculate('Td', **data) -273.15
Tv = atmos.calculate('Tv', **data)
data = {'Tv':Tv, 'rv':rv/1000., 'p':p*100.}
rho = atmos.calculate('rho', **data)

dpdz = rho * 9.8
heights = np.zeros_like(p)
heights[0] = 10.0
for i in range(1,len(heights)):
    heights[i] = ((((p[i-1] - p[i])*100.)) / dpdz[i-1]) + heights[i-1]

p=p*units.hPa45
T=T*units.degC
Td=Td*units.degC

fig = plt.figure(figsize=(9, 9))45
skew = SkewT(fig, rotation=45)

skew.plot(p, T, 'r',linewidth=2)
skew.plot(p, Td, 'g',linewidth=2)
skew.plot_barbs(p, u, v)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40,60)

cape, cin, prof = get_cape(filename,'ml')
print cape
prof = prof-273.15
skew.plot(p, prof, 'k')

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
#skew.ax.set_title('August 11')

plt.savefig('sounding1.png')
plt.close()


filename = 'KWAJEX_Soundings_17Aug1999/sounding_17aug1999_10mb_control.txt'
var = np.loadtxt(filename, dtype=float)
p = var[:,0]
T = var[:,1]
rv = var[:,2]*1000.
u = var[:,3]
v = var[:,4]


data = {'T':T+273.15, 'rv':rv/1000., 'p':p*100.}
Td = atmos.calculate('Td', **data) -273.15
Tv = atmos.calculate('Tv', **data)
data = {'Tv':Tv, 'rv':rv/1000., 'p':p*100.}
rho = atmos.calculate('rho', **data)

dpdz = rho * 9.8
heights = np.zeros_like(p)
heights[0] = 10.0
for i in range(1,len(heights)):
    heights[i] = ((((p[i-1] - p[i])*100.)) / dpdz[i-1]) + heights[i-1]

p=p*units.hPa
T=T*units.degC
Td=Td*units.degC


fig2 = plt.figure(figsize=(9, 9))

skew2 = SkewT(fig2, rotation=45)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew2.plot(p, T, 'r',linewidth=2)
skew2.plot(p, Td, 'g',linewidth=2)
skew2.plot_barbs(p, u, v)
skew2.ax.set_ylim(1000, 100)
skew2.ax.set_xlim(-40, 60)

cape, cin, prof = get_cape(filename,'ml')
print cape
prof = prof-273.15
skew2.plot(p, prof, 'k')

skew2.plot_dry_adiabats()
skew2.plot_moist_adiabats()
skew2.plot_mixing_lines()
#skew2.ax.set_title('August 17')
plt.savefig('sounding2.png')
plt.close()


filename = 'LBA_Soundings_23Feb1999/sounding_23feb1999_10mb_control.txt'
var = np.loadtxt(filename, dtype=float)
p = var[:,0]
T = var[:,1]
rv = var[:,2]
u = var[:,3]
v = var[:,4]


data = {'T':T+273.15, 'rv':rv/1000., 'p':p*100.}
Td = atmos.calculate('Td', **data) -273.15
Tv = atmos.calculate('Tv', **data)
data = {'Tv':Tv, 'rv':rv/1000., 'p':p*100.}
rho = atmos.calculate('rho', **data)

dpdz = rho * 9.8
heights = np.zeros_like(p)
heights[0] = 10.0
for i in range(1,len(heights)):
    heights[i] = ((((p[i-1] - p[i])*100.)) / dpdz[i-1]) + heights[i-1]

p=p*units.hPa
T=T*units.degC
Td=Td*units.degC


fig3 = plt.figure(figsize=(9, 9))

skew3 = SkewT(fig3, rotation=45)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew3.plot(p, T, 'r',linewidth=2)
skew3.plot(p, Td, 'g',linewidth=2)
skew3.plot_barbs(p, u, v)
skew3.ax.set_ylim(1000, 100)
skew3.ax.set_xlim(-40, 60)

cape, cin, prof = get_cape(filename,'ml')
print cape
prof = prof-273.15
skew3.plot(p, prof, 'k')

skew3.plot_dry_adiabats()
skew3.plot_moist_adiabats()
skew3.plot_mixing_lines()
#skew3.ax.set_title('February 23')
plt.savefig('sounding3.png')
plt.close()
# fig4,axes = plt.subplots(nrows=1,ncols=3)
# axes[0]=skew.ax
# axes[1]=skew2.ax
# axes[2]=skew3.ax

# Show the plot
#plt.savefig('sounding.png')
plt.figure(figsize=(10,4))
gs1 = gridspec.GridSpec(1,3)
gs1.update(wspace=0.025, hspace=0.025) # set the spacing between axes. 

# for i in range(16):
#    # i = i + 1 # grid spec indexes from 0
#     ax1 = plt.subplot(gs1[i])
#     plt.axis('on')
#     ax1.set_xticklabels([])
#     ax1.set_yticklabels([])
#     ax1.set_aspect('equal')
#     plt.subp


img1 = mpimg.imread('sounding1.png')
img2 = mpimg.imread('sounding2.png')
img3 = mpimg.imread('sounding3.png')

#fig,axes = plt.subplots(nrows=1,ncols=3)

ax = plt.subplot(gs1[0])#axes[0]
ax.axis('off')
ax.imshow(img1)
ax.set_title('August 11', fontweight = 'bold')

ax1 = plt.subplot(gs1[1])#axes[1]
ax1.axis('off')
ax1.imshow(img2)
ax1.set_title('August 17', fontweight = 'bold')

ax2 = plt.subplot(gs1[2])#axes[2]
ax2.axis('off')
ax2.imshow(img3)
ax2.set_title('February 23', fontweight = 'bold')

#plt.subplots_adjust(wspace=None, hspace=None)
#plt.show()
plt.savefig('sounding.png',format='png', dpi=200)




