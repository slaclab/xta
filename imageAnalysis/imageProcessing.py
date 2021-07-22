from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image

# Edit the list of filenames here. Filenames must be 2 characters in length or longer. 
# Valid extensions are .png , .jpg, .jfif, .jpeg, .tiff
# Pixel width should be 2.5mm(optimal)-5mm(minimal), to conform to the standards 
fileNames = ['jfif.slacerman.jfif','jpg.blackhole.jpg','png.slac.png','jpeg.seaturtle.jpeg','tiff.lab.tiff','png.test.png']

# A class to hold constant values
class Measure(object): 
    pass

# Get the parent directory
dirname = os.path.dirname(__file__)

# Create values for 1 CM.
CM1 = Measure()
CM1.pixels= 25                      # number of pixels to 1CM
CM1.inches = 0.393701               # number of inches in 1CM
CM1.dirname = dirname + '/1CM/'     # directory to store 1CM files

CM20 = Measure()
CM20.pixels = 500                   # number of pixels to 20CM
CM20.inches = 7.87402               # number of inches in 20CM
CM20.dirname = dirname +'/20CM/'    # directory to store 20CM files 

CM40 = Measure()
CM40.pixels = 1000                  # number of pixels to 40CM
CM40.inches = 15.748                # number of inches to 40CM
CM40.dirname = dirname + '/40CM/'   # directory to store 40CM files

# Bins are similar to resolution, too little and the image is pixelated, too many and the image is washed out
numBinsSmall = 200                  # Small Bin 
numBinsCustom = 250                 # Custom Value 
numBinsMedium = 500                 # Medium Bin 
numBinsLarge = 800                  # Large Bin 

dirnameOriginal = dirname + '/Original/'    # directory pointing to the Original file location, 'xta/imageAnalysis/Original/'
dirnameYaml = dirname + '/yaml/'            # directory pointing to the yaml file location, 'xta/imageAnalysis/yaml/'                 

#
# IMAGE PROCESSING TEMPLATE
#

for x in fileNames:
    filename = x
    im = Image.open(dirnameOriginal + filename)
    fileType = im.format
    # Create the dictionary information to insert into the .yaml file
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
    # If the file is .jpg format, fileType will report JPEG and so the file will have one less letter than it should
    # As long as files are 2 characters in length or greater, this will not be an issue
    filename = filename[:tLen-(len(fileType)+1)]
    # 'w' tag rewrites the file if it exists to save space, an easy way to preserve .yaml would be to 
    # check before this statement to add a number to the end of the filename
    with open((dirnameYaml + filename + '.in.yaml'),'w') as file:
        documents = yaml.dump(tempDictionary, file)

    # Resize and save image to 1cm x 1cm
    resized_im=im.resize((CM1.pixels, CM1.pixels))
    resized_im.save(CM1.dirname + filename + '.original.1cm.png')
    # Resize and save image to 20cm x 20cm
    resized_im=im.resize((CM20.pixels, CM20.pixels))
    resized_im.save(CM20.dirname + filename + '.original.20cm.png')
    # Resize and save image to 40cm x 40cm
    resized_im=im.resize((CM40.pixels, CM40.pixels))
    resized_im.save(CM40.dirname + filename + '.original.40cm.png')

    gen = Generator(dirnameYaml + filename + '.in.yaml',verbose=0)
    gen.run()

    pg = gen.particles
    pltx = pg.x
    plty = pg.y

    #1cm---------------------------------------------------------------------------------------------------------
    height = CM1.inches             # Height in inches
    aspect = 1                      # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)                 # Change bins here if needed

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    # Remove axis
    plt.gca().axis("off")

    figg=plt.gcf()
    # Set extent to make the image as big as possible with no borders
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM1.dirname + filename + '.1cm.png', bbox_inches=extent)

    #20cm------------------------------------------------------------------------------------------------------
    height = CM20.inches            # Height in inches
    aspect = 1                      # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)                 # Change bins here if needed

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    # Remove axis
    plt.gca().axis("off")

    figg=plt.gcf()
    # Set extent to make the image as big as possible with no borders
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM20.dirname + filename + '.20cm.png', bbox_inches=extent)

    #40cm-------------------------------------------------------------------------------------------------------
    height = CM40.inches            # Height in inches
    aspect = 1                      # height/width ratio
    width = height*aspect

    plt.figure(figsize=(width, height))
    figg=plt.hist2d(pltx,plty, bins = numBinsLarge)                 # Change bins here if needed

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
    # Remove axis
    plt.gca().axis("off")

    figg=plt.gcf()
    # Set extent to make the image as big as possible with no borders
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())
    figg.savefig(CM40.dirname + filename + '.40cm.png', bbox_inches=extent)

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------