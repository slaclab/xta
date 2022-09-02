import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('petrstyle.txt')
import glob, sys, h5py, os

from astra import Astra, template_dir
import distgen
from distgen import Generator
from distgen.writers import *
from pmd_beamphysics import ParticleGroup
from pmd_beamphysics.plot import marginal_plot
#slice plots
from h5py import File
from pmd_beamphysics.interfaces import opal
from pmd_beamphysics.plot import slice_plot
from pmd_beamphysics.plot import marginal_plot, density_plot

nbins = 100
#files = glob.glob('xta*_10pC_SC*laser_test*.h5')
files = glob.glob('archives/xta_60fs_1mm_10pC_SC_laser_weak_solenoid_0.4_zstop_5.5.h5')
fig,axs = plt.subplots(figsize = (6,6))

astra_file = 'xta.in'
xta = Astra(input_file=astra_file, astra_bin='/Users/nneveu/Code/astra/Astra', verbose=True)
xta.load_archive(files[0])
num  = len(xta.particles)

fig,axs = plt.subplots(figsize=(6,6))

nbins = 100
number_of_frames = num 

def update_hist(i):
    plt.cla()
    beam = xta.particles[i]
    X = beam.x*10**3 #np.random.randn(100000)
    Y = beam.y*10**3 #np.random.randn(100000) + 5
    plt.hist2d(X,Y, bins=100)
    axs.set_xlabel('x [mm]', size=15)
    axs.set_ylabel('y [mm]', size=15)
    axs.set_ylim(-2,2)
    axs.set_xlim(-2,2)

beam0 = xta.particles[0]
X0 = beam0.x*10**3 #np.random.randn(100000)
Y0 = beam0.y*10**3 #np.random.randn(100000) + 5

#Create 2d Histogram
hist = plt.hist2d([],[], bins=100)

animation = animation.FuncAnimation(fig, update_hist, np.arange(1,num) )
plt.show()



##Smooth with filter
#im = plt.imshow(data.T, interpolation = 'gaussian', origin = 'lower')
#
##Define animation. 
#def animate(i) :
#    beam = xta.particles[i]
#    X = beam.x*10**3 #np.random.randn(100000)
#    Y = beam.y*10**3 #np.random.randn(100000) + 5
#    data,x,y = np.histogram2d(X,Y, bins = nbins)
#    im.set_data(data)
#
#ani = animation.FuncAnimation(fig, animate, np.arange(0,num),
#                          interval = 100)
#
#plt.show()
