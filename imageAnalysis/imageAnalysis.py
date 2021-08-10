from matplotlib import pyplot as plt
from distgen import Generator
import yaml
import sys
import os
import h5py
import numpy as np
from PIL import Image, ImageChops
from numpy import asarray

# Get the parent directory
dirname = os.path.dirname(__file__)
# List the images the program can compare
testList = ['png.1-20.png', 'png.1-21.png', 'jfif.slacerman.jfif','jpg.blackhole.jpg','png.slac.png','jpeg.seaturtle.jpeg','tiff.lab.tiff','png.test.png']
# Which two images would you like to compare?
testData = [ 0, 1 ]
tDPath = 'testData' + str(testData[0]) + str(testData[1])
#  TESTS  #  FLAG TRUE TO PROCESS  #
# T1---------------------------------------------------------------------------------------------------------------------------------------------------
btest1 = True       # Add (img1 + img2) / (scale + offset)
t1Scale = 1.0       # Divided by Scale
t1Offset = 0        # When dividing(see above), a custom scale can be added to tScale before dividing
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T2---------------------------------------------------------------------------------------------------------------------------------------------------
btest2 = True       # Add Modulo (img1 + img2) % MAX
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T3---------------------------------------------------------------------------------------------------------------------------------------------------
btest3 = True       # Blend two images together. Creates a .gif, and a custom blend image.
t3Alpha = 1.0       # Set transparency weight
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T4 Composite ---------------------------------------------------------------------------------------------------------------------------------------------------
btest4 = True                       # Uses transparency mask.                    
maskList = ['png.testmask.png']     # List the masks to be considered for analysis
mask = maskList[0]                  # Select the mask from the maskList to be applied to the test
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T5 Darker ---------------------------------------------------------------------------------------------------------------------------------------------------
btest5 = True       # min(img1, img2) Compares pixel values and returns lower values.
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T6 Difference ---------------------------------------------------------------------------------------------------------------------------------------------------
btest6 = True       # |img1-img2| pixel by pixel difference
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T7 Invert channel values---------------------------------------------------------------------------------------------------------------------------------------------------
btest7 = True       #  MAX - img1
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T8 Lighter---------------------------------------------------------------------------------------------------------------------------------------------------
btest8 = True       #  Compare img1 and im2 pixel channel values and returns higher values
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T9 Logical AND ---------------------------------------------------------------------------------------------------------------------------------------------------
btest9 = True       # ((img1 AND img2) % MAX) Converts to 1 mode(1-bit pixels, black and white)
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T10 Logical OR ---------------------------------------------------------------------------------------------------------------------------------------------------
btest10 = True      # ((img1 OR img2) % MAX) Converts to 1 mode(1-bit pixels, black and white)
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T11 Logical XOR ---------------------------------------------------------------------------------------------------------------------------------------------------
btest11 = True      # ((img1 XOR img2) % MAX) Converts to 1 mode(1-bit pixels, black and white)
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T12 Multiply ---------------------------------------------------------------------------------------------------------------------------------------------------
btest12 = True      # (img1 * img2 / MAX) Superimposes 2 images on top of each other
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T13 Soft Light Algorithm ---------------------------------------------------------------------------------------------------------------------------------------------------
btest13 = True      # (2(img1)(img2) + img1^2(1-2(img2)) if img2<0.5 ; 2(img1)(1-img2)+sqrt(img1)(2(img2-1)) otherwise)
                    # Not sure if it's useful, but it's here.
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T14 Hard Light Algorithm ---------------------------------------------------------------------------------------------------------------------------------------------------
btest14 = True      # (2(img1)(img2) if img2<0.5 ; 1-2(1-img2)(1-img1) otherwise)
                    # Not sure if it is useful but it might be
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T15 Overlay ---------------------------------------------------------------------------------------------------------------------------------------------------
btest15 = True      # combination of multiply and screen. (2(img1)(img2) if img1 < 0.5 ; 1-2(1-img1)(1-img2) otherwise)
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T16 Screen ---------------------------------------------------------------------------------------------------------------------------------------------------
btest16 = True      # (MAX - ((MAX - img1) * (MAX - img2) / MAX))
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T17 Subtract ---------------------------------------------------------------------------------------------------------------------------------------------------
btest17 =  True     # ((img1 - img2) / scale + offset)
t17Scale = 1.0
t17Offset = 0
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# T18 Subtract Modulo ---------------------------------------------------------------------------------------------------------------------------------------------------
btest18 = True      # ((img1 - img2) % MAX)
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Create a dictionary for sizes I set it up like this so you could do Image.width() as a dictionary key.
# That way at a later date it could be used to more easily import files of any of the three variant sizes
sizes = {25:'1cm', 500:'20cm', 1000:'40cm'}





# PROCESS THE TEST IMAGES----------------------------------------------------------------------------------------------------------------------------

filename = testList[testData[0]] + '.' + testList[testData[1]]
fLen = len(filename)
fName = filename[:fLen-9]
# Open the images
img1 = Image.open(dirname + '/Original/' + testList[testData[0]] ).convert('RGBA').resize((768,768))
img2 = Image.open(dirname + '/Original/' + testList[testData[1]] ).convert('RGBA').resize((768,768))
print("test")
# Perform a series of tests on the images
# TEST1:ADD------------------------------------------------------------------------------------------------------------------------------------------
if btest1 == True:
    test1 = ImageChops.add(img1, img2, scale=t1Scale, offset=t1Offset)
    test1.save(dirname + '/Analysis/' + tDPath + '.' + fName + '.' + '.add.png')

# TEST2:ADD_MODULO-----------------------------------------------------------------------------------------------------------------------------------
if btest2 == True:
    test2 = ImageChops.add_modulo(img1, img2)
    test2.save(dirname + '/Analysis/' + tDPath + '.' + fName + '.' + '.add_modulo.png')

# TEST3:BLEND----------------------------------------------------------------------------------------------------------------------------------------
# Testing making a gif. Credit to hhsprings.bitbucket.io for the general model.
if btest3 == True:
    frames = [
        ImageChops.blend(
            img1, img2, alpha = 1.0 / 32 * i)
        for i in range(32+1)
        ]
    frames[0].save(
        dirname + '/Analysis/' + tDPath + '.' + fName + '.blend.gif',
        save_all = True,
        append_images = frames[1:],
        optimize = True,
        duration = 100,
        loop = 255) 
    test3 = ImageChops.blend(img1, img2, alpha = t3Alpha)
    test3.save(dirname + '/Analysis/' + tDPath + '.' + fName + '.blend.png')

# TEST4:COMPOSITE------------------------------------------------------------------------------------------------------------------------------------
if btest4 == True:
# FIRST PROCESS ANY MASKS----------------------------------------------------------------------------------------------------------------------------
    for x in maskList:
        tLen = len(x)
        xType = Image.open(dirname + '/masks/original/' + mask).format
        # If the file is .jpg format, fileType will report JPEG and so the file will have one less letter than it should
        # As long as files are 2 characters in length or greater, this will not be an issue
        filename = x[:tLen - (len(xType) + 1)]
        tMask = Image.open(dirname + '/masks/original/' + x).resize((768,768))
        tMask = tMask.save(dirname + '/masks/resized/' + filename + '.resized.' + xType.lower())
# ---------------------------------------------------------------------------------------------------------------------------------------------------
    test4 = ImageChops.composite(img1, img2, tMask)
    test4.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.composite.png')

# TEST5:DARKER---------------------------------------------------------------------------------------------------------------------------------------
if btest5 == True:
    test5 = ImageChops.darker(img1, img2)
    test5.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.darker.png')

# TEST6:DIFFERENCE-----------------------------------------------------------------------------------------------------------------------------------
if btest6 == True:
    # Difference Analysis requires the file to be in "RGB" mode.
    ttImg1 = img1.convert("RGB")
    ttImg2 = img2.convert("RGB")
    test6 = ImageChops.difference(ttImg1, ttImg2)
    test6.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.difference.png')

# TEST7:INVERT---------------------------------------------------------------------------------------------------------------------------------------
if btest7 == True:
    # Inverse Analysis requires the file to be in "RGB" mode.
    test7 = ImageChops.invert(ttImg1)
    test7.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.invert.png')

# TEST8:LIGHTER--------------------------------------------------------------------------------------------------------------------------------------
if btest8 == True:
    test8 = ImageChops.lighter(img1, img2)
    test8.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.lighter.png')

# TEST9:LOGICAL_AND----------------------------------------------------------------------------------------------------------------------------------
if btest9 == True:
    # Logical analysis requires the file be in mode "1"
    tImg1 = img1.convert("1")
    tImg2 = img2.convert("1")
    test9 = ImageChops.logical_and(tImg1, tImg2)
    test9.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.logical_and.png')

# TEST10:LOGICAL_OR----------------------------------------------------------------------------------------------------------------------------------
if btest10 == True:
    # Logical analysis requires the file be in mode "1"
    test10 = ImageChops.logical_or(tImg1, tImg2)
    test10.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.logical_or.png')

# TEST11:LOGICAL_XOR---------------------------------------------------------------------------------------------------------------------------------
if btest11 == True:
    # Logical analysis requires the file be in mode "1"
    test11 = ImageChops.logical_xor(tImg1, tImg2)
    test11.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.logical_xor.png')

# TEST12:MULTIPLY------------------------------------------------------------------------------------------------------------------------------------
if btest12 == True:
    test12 = ImageChops.multiply(img1, img2)
    test12.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.multiply.png')

# TEST13:SOFT LIGHT ALGORITHM------------------------------------------------------------------------------------------------------------------------
if btest13 == True:
    test13 = ImageChops.soft_light(img1, img2)
    test13.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.soft_light.png')

# TEST14:HARD LIGHT ALGORITHM------------------------------------------------------------------------------------------------------------------------
if btest14 == True:
    test14 = ImageChops.hard_light(img1, img2)
    test14.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.hard_light.png')

# TEST15:OVERLAY ALGORITHM---------------------------------------------------------------------------------------------------------------------------
if btest15 == True:
    test15 = ImageChops.overlay(img1, img2)
    test15.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.overlay.png')

# TEST16:SCREEN--------------------------------------------------------------------------------------------------------------------------------------
if btest16 == True:
    test16 = ImageChops.screen(img1, img2)
    test16.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.screen.png')

# TEST17:SUBTRACT------------------------------------------------------------------------------------------------------------------------------------
if btest17 == True:
    # Subtractive Analysis requires the file to be in "RGB" mode.
    test17 = ImageChops.subtract(ttImg1, ttImg2, scale = t17Scale, offset = t17Offset)
    test17.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.subtract.png')

# TEST18:SUBTRACT_MODULO-----------------------------------------------------------------------------------------------------------------------------
if btest18 == True:
    # Subtractive Analysis requires the file to be in "RGB" mode.
    test18 = ImageChops.subtract_modulo(ttImg1, ttImg2)
    test18.save(dirname + '/Analysis/'   + tDPath + '.' + fName +    '.subtract_modulo.png')
# ---------------------------------------------------------------------------------------------------------------------------------------------------