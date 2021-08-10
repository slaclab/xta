from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image
from pdf2image import convert_from_path

# Edit the list of filenames here. Filenames must be 2 characters in length or longer. 
# Valid extensions are .png , .jpg, .jfif, .jpeg, .tiff
# Pixel width should be 2.5mm(optimal)-5mm(minimal), to conform to the standards 
fileNames = ['edit1-20.pdf' , 'edit1-21.pdf' , 'jfif.slacerman.jfif','jpg.blackhole.jpg','png.slac.png','jpeg.seaturtle.jpeg','tiff.lab.tiff','png.test.png']

# A class to hold constant values
class Measure(object): 
    pass

# Get the parent directory
dirname = os.path.dirname(__file__)
count = 0
for x in fileNames:
    if x[len(x)-3] == 'p' and x[len(x)-2] == 'd' and x[len(x)-1] == 'f':
        pdf = convert_from_path(dirname +'/Original/'+ x)
        print(pdf)
        for q in range(len(pdf)):
            pdf[q].save(dirname + '/Original/' + 'png.' + x + '.'+ str((q+1)) + '.png','PNG')
        fileNames[count] = 'png.' + x + '.' + str((q + 1)) + '.png'  
    count+=1

# Bins are similar to resolution, too little and the image is pixelated, too many and the image is washed out
# There are optimization functions for 1D histograms but not 2D.
numBinsSmall = 200                  # Small Bin 
numBinsCustom = 250                 # Custom Value 
numBinsMedium = 500                 # Medium Bin 
numBinsLarge = 800                  # Large Bin 
# Edit this to change the Bin count without having to go through every line and change it.
tBins = numBinsMedium
# Edit this to change the number of particles coded into the .yaml file.
n_particles= 1000000
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
    tempDictionary = {'n_particle': n_particles,
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

    resized_im = im.resize((768,768))     # Resize and save image to 768 x 768
    resized_im.save(dirname + '/Processed/' + filename + '.original.768.png')

    gen = Generator(dirnameYaml + filename + '.in.yaml',verbose=0)
    gen.run()

    pg = gen.particles
    pltx = pg.x
    plty = pg.y

    #40cm-------------------------------------------------------------------------------------------------------
    height = 7.68                                           # Height in inches
    aspect = 1                                              # height/width ratio
    width = height*aspect

    plt.figure(figsize = (width, height))
    figg=plt.hist2d(pltx, plty, bins = tBins)                # Change bins here if needed

    plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
  
    plt.gca().axis("off")                                   # Remove axis

    figg=plt.gcf()
    
    extent = figg.get_window_extent().transformed(figg.dpi_scale_trans.inverted())  # Set extent to make the image as big as possible with no borders
    figg.savefig(dirname + '/Processed/' + filename + '.768.png', bbox_inches=extent)

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------