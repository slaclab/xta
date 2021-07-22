from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image

#-------------------------------------------------

img1 = Image.open('examples/data/png.brule.png')
img2 = Image.open('brule.png')


dif = np.fabs(np.subtract(img2[:], img1[:]))
imgplot = plt.imshow(dif)
imgplot.set_cmap('jet')
plt.axis('off')
figg=plt.gcf()
extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
figg.savefig('brulecompare.png', bbox_inches=extent)