from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image

fileNames = ['jfif.slacerman.jfif','jpg.blackhole.jpg','png.slac.png','jpeg.seaturtle.jpeg','tiff.lab.tiff','png.test.png']

class Measure(object): 
    pass

dirname = os.path.dirname(__file__)

CM1 = Measure()
CM1.pixels= 25
CM1.inches = 0.393701
CM1.dirname = dirname + '/1CM/'

CM20 = Measure()
CM20.pixels = 500
CM20.inches = 7.87402
CM20.dirname = dirname +'/20CM/'

CM40 = Measure()
CM40.pixels = 1000
CM40.inches = 15.748
CM40.dirname = dirname + '/40CM/'

numBinsSmall = 200 #Small
numBinsCustom = 250 #Custom Value
numBinsMedium = 500 #Medium
numBinsLarge = 800 #Large

dirnameOriginal = dirname + '/Original/'
dirnameYaml = dirname + '/yaml/'
savedirname = dirname + ''

#
#GENERIC
#
for x in fileNames:
    filename = x
    im = Image.open(dirnameOriginal + filename)
    fileType = im.format
    tempDictionary = {'n_particle': 1000000,
                'output': {'file': 'rad.uniform.out.txt', 'type': 'gpt'},
                'random_type': 'hammersley', 
                'start': {'MTE': {'units': 'meV', 'value': 150}, 'type': 'cathode'},
                'total_charge': {'units': 'pC', 'value': 10},
                'xy_dist': {'file': dirnameOriginal + filename, 'type': 'file2d',
                    'min_x': {'value': -1, 'units': 'mm'},
                    'max_x': {'value': 1, 'units': 'mm'},
                    'min_y': {'value': -1, 'units': 'mm'},
                    'max_y': {'value': 1, 'units': 'mm'},
                    'threshold': 0.0}}
    # write to file, if one exists, overwrite it.
    tLen = len(filename)
    filename = filename[:tLen-(len(fileType)+1)]
    with open((dirnameYaml + filename + '.in.yaml'),'w') as file:
        documents = yaml.dump(tempDictionary, file)

    #tLen = len(filename)
    #filename = filename[:tLen-(len(fileType)+1)]

    #1cm
    resized_im=im.resize((CM1.pixels, CM1.pixels))
    resized_im.save(CM1.dirname + filename + '.original.1cm.png')
    #20cm
    resized_im=im.resize((CM20.pixels, CM20.pixels))
    resized_im.save(CM20.dirname + filename + '.original.20cm.png')
    #40cm
    resized_im=im.resize((CM40.pixels, CM40.pixels))
    resized_im.save(CM40.dirname + filename + '.original.40cm.png')

    gen = Generator(dirnameYaml + filename + '.in.yaml',verbose=0)
    gen.run()

    pg = gen.particles
    pltx = pg.x
    plty = pg.y

    #1cm---------------------------------------------------------------------------------------------------------
    height = CM1.inches # inch
    aspect = 1 # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    plt.gca().axis("off")

    figg=plt.gcf()
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM1.dirname + filename + '.1cm.png', bbox_inches=extent)

    #20cm------------------------------------------------------------------------------------------------------
    height = CM20.inches # inch
    aspect = 1 # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    plt.gca().axis("off")

    figg=plt.gcf()
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM20.dirname + filename + '.20cm.png', bbox_inches=extent)

    #40cm-------------------------------------------------------------------------------------------------------
    height = CM40.inches # inch
    aspect = 1 # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    plt.gca().axis("off")

    figg=plt.gcf()
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM40.dirname + filename + '.40cm.png', bbox_inches=extent)

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------


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