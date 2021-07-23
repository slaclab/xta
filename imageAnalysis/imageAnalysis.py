from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image, ImageChops
from numpy import asarray

# Pillow has some functionality for this!------------------------------------------------------------------------------------------------------------
# Get the parent directory
dirname = os.path.dirname(__file__)
testList = ['jfif.slacerman.20cm.png','jpg.blackhol.20cm.png','png.slac.20cm.png','jpeg.seaturtle.20cm.png','tiff.lab.20cm.png','png.test.20cm.png']
# Create a dictionary for sizes
sizes = {25:'1cm', 500:'20cm', 1000:'40cm'}
# FIRST PROCESS ANY MASKS----------------------------------------------------------------------------------------------------------------------------
# Add any new masks to this list and they will be converted to be applied to images.
maskList = ['png.testmask.png']
mask1 = []
mask20 = []
mask40 = []
for x in maskList:
    print(x)
    tLen = len(x)
    xType = Image.open(dirname + '/masks/original/' + x).format
    print(xType)
    # If the file is .jpg format, fileType will report JPEG and so the file will have one less letter than it should
    # As long as files are 2 characters in length or greater, this will not be an issue
    filename = x[:tLen - (len(xType) + 1)]
    tMask = Image.open(dirname + '/masks/original/' + x).resize((25,25))
    mask1.append(tMask)
    tMask = tMask.save(dirname + '/masks/1CM/' + filename + '.1CM.' + xType.lower())
    tMask = Image.open(dirname + '/masks/original/' + x).resize((500,500))
    mask20.append(tMask)
    tMask = tMask.save(dirname + '/masks/20CM/' + filename + '.20CM.' + xType.lower())
    tMask = Image.open(dirname + '/masks/original/' + x).resize((1000,1000))
    mask40.append(tMask)
    tMask = tMask.save(dirname + '/masks/40CM/' + filename + '.40CM.' + xType.lower())
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# PROCESS THE TEST IMAGES----------------------------------------------------------------------------------------------------------------------------
for x in testList:
    filename = x
    fLen = len(filename)
    fName = filename[:fLen-9]
    # Open the images
    img1 = Image.open(dirname + '/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.png').convert('RGBA')
    #print(img1.mode)
    img2 = Image.open(dirname + '/' + sizes[500].upper() + '/' + fName + '.original.' + sizes[500] + '.png').convert('RGBA')
    #print(img2.mode)
# Perform a series of tests on the images
# TEST1:ADD------------------------------------------------------------------------------------------------------------------------------------------
    tScale = 1.0    # Divided by Scale
    tOffset = 0   # When dividing(see above), a custom scale can be added to tScale before dividing
    test1 = ImageChops.add(img1, img2, scale=tScale, offset=tOffset)
    test1.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.add.png')
# TEST2:ADD_MODULO-----------------------------------------------------------------------------------------------------------------------------------
    test2 = ImageChops.add_modulo(img1, img2)
    test2.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.add_modulo.png')
# TEST3:BLEND----------------------------------------------------------------------------------------------------------------------------------------
    # Testing making a gif. Credit to hhsprings.bitbucket.io for the general model.
    frames = [
        ImageChops.blend(
            img1, img2, alpha = 1.0 / 32 * i)
        for i in range(32+1)
        ]
    frames[0].save(
        dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.blend.gif',
        save_all = True,
        append_images = frames[1:],
        optimize = True,
        duration = 100,
        loop = 255)
    tAlpha = 1.0
    test3 = ImageChops.blend(img1, img2, alpha = tAlpha)
    test3.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.blend.png')
# TEST4:COMPOSITE------------------------------------------------------------------------------------------------------------------------------------
    mask = mask20[0]
    test4 = ImageChops.composite(img1, img2, mask)
    test4.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.composite.png')
# TEST5:DARKER---------------------------------------------------------------------------------------------------------------------------------------
    test5 = ImageChops.darker(img1, img2)
    test5.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.darker.png')
# TEST6:DIFFERENCE-----------------------------------------------------------------------------------------------------------------------------------
    test6 = ImageChops.difference(img1, img2)
    test6.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.difference.png')
# TEST7:INVERT---------------------------------------------------------------------------------------------------------------------------------------
    test7 = ImageChops.invert(img1)
    test7.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.invert.png')
# TEST8:LIGHTER--------------------------------------------------------------------------------------------------------------------------------------
    test8 = ImageChops.lighter(img1, img2)
    test8.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.lighter.png')
# TEST9:LOGICAL_AND----------------------------------------------------------------------------------------------------------------------------------
    # Logical analysis requires the file be in mode "1"
    tImg1 = img1.convert("1")
    tImg2 = img2.convert("1")
    test9 = ImageChops.logical_and(tImg1, tImg2)
    test9.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.logical_and.png')
# TEST10:LOGICAL_OR----------------------------------------------------------------------------------------------------------------------------------
    # Logical analysis requires the file be in mode "1"
    test10 = ImageChops.logical_or(tImg1, tImg2)
    test10.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.logical_or.png')
# TEST11:LOGICAL_XOR---------------------------------------------------------------------------------------------------------------------------------
    # Logical analysis requires the file be in mode "1"
    test11 = ImageChops.logical_xor(tImg1, tImg2)
    test11.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.logical_xor.png')
# TEST12:MULTIPLY------------------------------------------------------------------------------------------------------------------------------------
    test12 = ImageChops.multiply(img1, img2)
    test12.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.multiply.png')
# TEST13:SOFT LIGHT ALGORITHM------------------------------------------------------------------------------------------------------------------------
    test13 = ImageChops.soft_light(img1, img2)
    test13.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.soft_light.png')
# TEST14:HARD LIGHT ALGORITHM------------------------------------------------------------------------------------------------------------------------
    test14 = ImageChops.hard_light(img1, img2)
    test14.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.hard_light.png')
# TEST15:OVERLAY ALGORITHM---------------------------------------------------------------------------------------------------------------------------
    test15 = ImageChops.overlay(img1, img2)
    test15.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.overlay.png')
# TEST16:SCREEN--------------------------------------------------------------------------------------------------------------------------------------
    test16 = ImageChops.screen(img1, img2)
    test16.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + fName + '.' + sizes[500] + '.screen.png')
# TEST17:SUBTRACT------------------------------------------------------------------------------------------------------------------------------------
    tScale = 1.0
    test17 = ImageChops.subtract(img1, img2, scale = tScale)
    test17.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + filename + '.' + sizes[500] + '.subtract.png')
# TEST18:SUBTRACT_MODULO-----------------------------------------------------------------------------------------------------------------------------
    test18 = ImageChops.subtract_modulo(img1, img2)
    test18.save(dirname + '/Analysis/' + sizes[500].upper() + '/' + filename + '.' + sizes[500] + '.subtract_modulo.png')
# ---------------------------------------------------------------------------------------------------------------------------------------------------