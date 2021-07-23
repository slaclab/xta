from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image, ImageChops
from numpy import asarray

#-------------------------------------------------
# Get the parent directory
dirname = os.path.dirname(__file__)
filename = 'x'
sizes = {25:'1cm', 500:'20cm', 1000:'40cm'}
img1 = Image.open(dirname + '/20CM/png.test.20cm.png')
img2 = Image.open(dirname + '/20CM/png.test.original.20cm.png')

test1 = ImageChops.add(img1, img2)
test1.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.add.png')
test2 = ImageChops.composite(img1,img2)
test2.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.composite.png')
test3 = ImageChops.difference(img1,img2)
test3.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.difference.png')
test4 = ImageChops.logical_and(img1,img2)
test4.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.logical_and.png')
test5 = ImageChops.logical_or(img1,img2)
test5.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.logical_or.png')
test6 = ImageChops.logical_xor(img1,img2)
test6.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.logical_xor.png')
test7 = ImageChops.multiply(img1,img2)
test7.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.multiply.png')
test8 = ImageChops.subtract(img1,img2)
test8.save(dirname + '/Analysis/20CM/' + filename + '.'+ sizes[500] +'.subtract.png')

numpy1 = asarray(img1)
numpy2 = asarray(img2)

dif = np.fabs(np.subtract(numpy2[:], numpy1[:]))
imgplot = plt.imshow(dif)
imgplot.set_cmap('jet')
plt.axis('off')
figg=plt.gcf()
extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
figg.savefig('brulecompare.png', bbox_inches=extent)