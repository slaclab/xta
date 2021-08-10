import numpy as np
from numpy.random import normal
from scipy import linspace
import array
from matplotlib import rcParams
from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
from PIL import Image, ImageChops
from numpy import asarray

from matplotlib.pyplot import figure,  plot, xlabel, ylabel,\
    title, show, savefig, hist

n_particles= 1000000
dirname = os.path.dirname(__file__)

filename = 'tiff.lab.tiff'
im = Image.open(filename)
fileType = im.format
# Create the dictionary information to insert into the .yaml file
tempDictionary = {'n_particle': n_particles,
            'output': {'file': 'rad.uniform.out.txt', 'type': 'gpt'},
            'random_type': 'hammersley', 
            'start': {'MTE': {'units': 'meV', 'value': 150}, 'type': 'cathode'},
            'total_charge': {'units': 'pC', 'value': 10},
            'xy_dist': {'file': filename, 'type': 'file2d',
                'min_x': {'value': -1, 'units': 'mm'},
                'max_x': {'value': 1, 'units': 'mm'},
                'min_y': {'value': -1, 'units': 'mm'},
                'max_y': {'value': 1, 'units': 'mm'},
                'threshold': 0.0}}
# write to file, if one exists, overwrite it.
tLen = len(filename)
# If the file is .jpg format, fileType will report JPEG and so the file will have one less letter than it should
# As long as files are 2 characters in length or greater, this will not be an issue
filename = filename[:tLen-(len(fileType)+1)]
# 'w' tag rewrites the file if it exists to save space, an easy way to preserve .yaml would be to 
# check before this statement to add a number to the end of the filename
with open((dirname + filename + '.in.yaml'),'w') as file:
    documents = yaml.dump(tempDictionary, file)

gen = Generator(dirname + filename + '.in.yaml',verbose=0)
gen.run()

pg = gen.particles
pltx = pg.x
plty = pg.y

x_min = np.min(pltx)
x_max = np.max(pltx)
y_min = np.min(plty)
y_max = np.max(plty)
x_bins = np.linspace(x_min,x_max, 768)
y_bins = np.linspace(y_min, y_max, 768)

print('xbins' + str(x_bins))
print('ybins' + str(y_bins))
height = 8            # Height in inches
aspectr = 1                      # height/width ratio
width = height*aspectr

plt.figure(figsize=(width, height))
figg=plt.hist2d(pltx,plty, bins = [x_bins,y_bins])                 # Change bins here if needed

plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
# Remove axis
plt.gca().axis("off")

figg=plt.gcf()
# Set extent to make the image as big as possible with no borders
extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
figg.savefig(dirname + filename + '.20cm.png', bbox_inches=extent, dpi=81.28)