import numpy as np
import matplotlib.pyplot as plt
plt.style.use('petrstyle.txt')

import glob, sys, h5py, os
import seaborn as sns
sys.path.insert(0, os.path.abspath('/Users/nneveu/github/lume-astra'))
sys.path.insert(0, os.path.abspath('/Users/nneveu/github/distgen'))

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

import os
import ffmpeg
#import subprocess
#from matplotlib.animation import FuncAnimation #, PillowWriter
import matplotlib.animation as animation

nbins = 100
#files = glob.glob('xta*_10pC_SC*laser_test*.h5')
files = glob.glob('archives/xta_60fs_1mm_10pC_SC_laser_weak_solenoid_0.4_zstop_5.5.h5')
#plt.subplots_adjust(left=0.25, bottom=0.1, right=0.75 , top=0.9, wspace=0.6, hspace=0.45)
fig,axs = plt.subplots(figsize = (6,6))

astra_file = 'xta.in'
xta = Astra(input_file=astra_file, astra_bin='/Users/nneveu/Code/astra/Astra', verbose=True)
xta.load_archive(files[0])
num  = len(xta.particles)
beam = xta.particles[0] 

#https://stackoverflow.com/questions/48395209/how-to-animate-an-image-derived-from-a-2d-histogram

X = beam.x #np.random.randn(100000)
Y = beam.y #np.random.randn(100000) + 5

#Create 2d Histogram
data,x,y = np.histogram2d(X,Y, bins = 100)

#Smooth with filter
im = plt.imshow(data.T, interpolation = 'gaussian', origin = 'lower')

#Define animation. 
def animate(i) :
    beam = xta.particles[i]
    X = beam.x*10**3 #np.random.randn(100000)
    Y = beam.y*10**3 #np.random.randn(100000) + 5
    data,x,y = np.histogram2d(X,Y, bins = 100)
    axs.set_xlabel('x [mm]', size=15)
    axs.set_ylabel('y [mm]', size=15)
    axs.set_ylim(-2,2)
    axs.set_xlim(-2,2)
    im.set_data(data.T)

ani = animation.FuncAnimation(fig, animate, np.arange(1,num), interval = 100, blit = False)

plt.show()

 
#    z = np.mean(xta.particles[i].z)
#    axs.hist2d(s.x*10**3, s.y*10**3, bins = nbins, cmin=1) #cmap='YlGnBu')
#    title = 'z = ' + str(z)
#    axs.set_title(title, size=15)
    #axs.set_title( 'z = %1.5f m', z)#keyname + ', z = %1.2f m' %np.mean(s['z']))
#    #fig.suptitle('z = %1.10f m' %np.mean(s['z']),fontsize=16)
#    return axs
#
#ani = FuncAnimation(fig, animate, range(num))#, init_func=plt.clf()) #407
#ani.save("10pC_sol_0.4_SC_laser_movie.mp4") #, writer=animation.FFMpegWriter(fps=2)) # writer=PillowWriter(fps=3))
##plt.show()
