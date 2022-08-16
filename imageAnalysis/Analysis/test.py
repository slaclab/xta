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
t2021 = '1-20VS1-21'
t21 = 'genVSoriginal1-21'
t20 = 'genVSoriginal1-20'
testList = ['png.testData01.1-21.1-20.difference.png', 
            'png.testData01.1-21.x.original.difference.png', 
            'png.testData01.1-20.x.original.difference.png']

img1 = Image.open(dirname + '/' + t2021 + '/' + testList[0])
img2 = Image.open(dirname + '/' + t20 + '/' + testList[2])
img3 = Image.open(dirname + '/' + t21 + '/' + testList[1])

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# img1 Analysis
pixels1 = list(img1.getdata())
lPixels1 = len(pixels1)
values1 = []
sumPixels1 = []

for x in pixels1:
    xx = sum(x)
    sumPixels1.append(xx)
    values1.append(x[0])
    values1.append(x[1])
    values1.append(x[2])
    
lValues1 = len(values1)

#-----------------------------------------------------------------------------------------------------------
# % of non zero pixel
zPixel1 = 0
for x in pixels1:
    res = sum(x)
    if res == 0:
        zPixel1 += 1
nZPixel1 = lPixels1 - zPixel1
statNZPixel1 = round(((nZPixel1/lPixels1) * 100), 2)
print('statNZPixel1: ' + str(statNZPixel1))
# print('zPixel1: ' + str(zPixel1))   
# print('lPixels1: ' + str(lPixels1)) 

#-----------------------------------------------------------------------------------------------------------
# % of non zero channel
zChannel1 = 0
for x in values1:
    if x == 0:
        zChannel1 +=1
nZChannel1 = lValues1 -zChannel1
statNZChannel1 = round(((nZChannel1/lValues1) * 100), 2)
print('statNZChannel1: ' + str(statNZChannel1))

#-----------------------------------------------------------------------------------------------------------
# Biggest % change by channel
bigChannel1 = 0
for x in values1:
    if x > bigChannel1:
        bigChannel1 = x
print('bigChannel1: ' + str(bigChannel1))
statChannel1 = round(((bigChannel1/255) * 100), 2)
print('statChannel1: ' + str(statChannel1))

#-----------------------------------------------------------------------------------------------------------
# Biggest % change in a sumpixel
bigPixel1 = 0
for x in sumPixels1:
    if x > bigPixel1:
        bigPixel1 = x
print('bigPixel1: ' + str(bigPixel1))
statPixel1 = round(((bigPixel1/765) * 100), 2)
print('statPixel1: ' + str(statPixel1))

#-----------------------------------------------------------------------------------------------------------
# pie chart frequency of % change by channel
statChannelList1 = []
for x in values1:
    xx = round(((x/255) * 100), 0)
    statChannelList1.append(xx)
statChannelList1.sort()
lStatChannelList1 = len(statChannelList1)

sTotal= 0
for x in range(0,101):
    if statChannelList1.count(x)>0:
        xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
        # print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
# print(sTotal)

r05 = 0
for x in range(0,5):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r05 = r05 + xx
# print('r05: ' + str(r05))

r525 = 0
for x in range(5,25):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r525 = r525 + xx
# print('r525: ' + str(r525))

r2544 = 0
for x in range(25,44):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r2544 = r2544 + xx
# print('r2544: ' + str(r2544))

r4463 = 0
for x in range(44,63):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r4463 = r4463 + xx
# print('r4463: ' + str(r4463))

r6382 = 0
for x in range(63,82):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r6382 = r6382 + xx
# print('r6382: ' + str(r6382))

r82101 = 0
for x in range(82,101):
    xx = round((((statChannelList1.count(x))/lStatChannelList1) * 100),2)
    r82101 = r82101 + xx
# print('r82101: ' + str(r82101))

orderedChannelStatList1 = [56.03, 28.14, 9.19, 4.41, 1.38, 0.85]
pieLabels1 = ['Under 5%','5-24%','25-43%','44-62%','63-81%','82-100%']
explodeTuple1 = (0.1, 0.0, 0.0, 0.0, 0.2, 0.4)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedChannelStatList1,
                explode = explodeTuple1,
                labels = pieLabels1,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=90)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartChannel1.png', transparent = True)

#-----------------------------------------------------------------------------------------------------------
# pie chart frequency of % change by pixel
statPixelList1 = []
for x in sumPixels1:

    if x == 0:
        statPixelList1.append(x)
    else:
        xx = round(((x/765) * 100), 0)
        statPixelList1.append(xx)
statPixelList1.sort()
lStatPixelList1 = len(statPixelList1)
# print('lStatPixelList1: ' + str(lStatPixelList1))

sTotal = 0
# More 0 here because zPixel is only 0 and these can round to 0.
for x in range(0,101):
    if statPixelList1.count(x)>0:
        #print('pixel count of ' + str(x) + ': ' + str(statPixelList1.count(x)))
        xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
        # print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
# print(sTotal)

r01 = 0
for x in range(0, 1):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r01 = r01 + xx
#print('r01: ' + str(r01))

r16 = 0
for x in range(1, 6):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r16 = r16 + xx
#print('r16: ' + str(r16))

r616 = 0
for x in range(6, 16):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r616 = r616 + xx
#print('r616: ' + str(r616))

r1631 = 0
for x in range(16,31):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r1631 = r1631 + xx
#print('r1631: ' + str(r1631))

r3146 = 0
for x in range(31, 46):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r3146 = r3146 + xx
#print('r3146: ' + str(r3146))

r4661 = 0
for x in range(46, 61):
    xx = round((((statPixelList1.count(x))/lStatPixelList1) * 100),2)
    r4661 = r4661 + xx
#print('r4661: ' + str(r4661))

orderedPixelStatList1 = [40.82, 12.26, 16.74, 18.71, 7.36, 4.11]
pieLabels1 = ['0','1-5%','6-15%','16-30%','31-45%','46-60%']
explodeTuple1 = (0.1, 0.1, 0.0, 0.0, 0.0, 0.0)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedPixelStatList1,
                explode = explodeTuple1,
                labels = pieLabels1,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=90)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartPixel1.png', transparent = True)

#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# img2 Analysis
pixels2 = list(img2.getdata())
lPixels2 = len(pixels2)
values2 = []
sumPixels2 = []
count = 0
for x in pixels2:
    xx = sum(x)
    if xx == 153:
        count+=1
    else:
        sumPixels2.append(xx)
    if x[0] == 68 and x[1] == 1 and x[2] == 84:
        foo = 0
    else:    
        values2.append(x[0])
        values2.append(x[1])
        values2.append(x[2])
lValues2 = len(values2)

#-----------------------------------------------------------------------------------------------------------
# % of non zero pixel
zPixel2 = 0
for x in pixels2:
    res = sum(x)
    if res == 0:
        zPixel2 += 1
nZPixel2 = lPixels2 - zPixel2
statNZPixel2 = round(((nZPixel2/lPixels2) * 100), 2)
print('statNZPixel2: ' + str(statNZPixel2))

#-----------------------------------------------------------------------------------------------------------
# % of non zero channel
zChannel2 = 0
for x in values2:
    if x == 0:
        zChannel2 +=1
nZChannel2 = lValues2 -zChannel2
statNZChannel2 = round(((nZChannel2/lValues2) * 100), 2)
print('statNZChannel2: ' + str(statNZChannel2))

#-----------------------------------------------------------------------------------------------------------
# Biggest % change by channel
bigChannel2 = 0
for x in values2:
    if x > bigChannel2:
        bigChannel2 = x
print('bigChannel2: ' + str(bigChannel2))
statChannel2 = round(((bigChannel2/255) * 100), 2)
print('statChannel2: ' + str(statChannel2))

#-----------------------------------------------------------------------------------------------------------
# Biggest % change in a sumpixel
bigPixel2 = 0
for x in sumPixels2:
    if x > bigPixel2:
        bigPixel2 = x
print('bigPixel2: ' + str(bigPixel2))
statPixel2 = round(((bigPixel2/765) * 100), 2)
print('statPixel2: ' + str(statPixel2))

#-----------------------------------------------------------------------------------------------------------
# pie chart frequency of % change by channel
statChannelList2 = []
for x in values2:
    xx = round(((x/255) * 100), 0)
    statChannelList2.append(xx)
statChannelList2.sort()
lStatChannelList2 = len(statChannelList2)

sTotal= 0
for x in range(0,101):
    if statChannelList2.count(x)>0:
        xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
        #print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
#print(sTotal)

r01 = 0
for x in range(0,1):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r01 = r01 + xx
#print('r01: ' + str(r01))

r16 = 0
for x in range(1,6):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r16 = r16 + xx
#print('r16: ' + str(r16))

r626 = 0
for x in range(6,26):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r626 = r626 + xx
#print('r626: ' + str(r626))

r2651 = 0
for x in range(26,51):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r2651 = r2651 + xx
#print('r2651: ' + str(r2651))

r5176 = 0
for x in range(51,76):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r5176 = r5176 + xx
#print('r5176: ' + str(r5176))

r76101 = 0
for x in range(76,101):
    xx = round((((statChannelList2.count(x))/lStatChannelList2) * 100),2)
    r76101 = r76101 + xx
#print('r76101: ' + str(r76101))

orderedChannelStatList2 = [16.53, 9.87, 20.74, 43.73, 4.11, 5.02]
pieLabels2 = ['0%','1-5%','6-25%','26-50%','51-75%','76-100%']
explodeTuple2 = (0.1, 0.1, 0.0, 0.0, 0.0, 0.0)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedChannelStatList2,
                explode = explodeTuple2,
                labels = pieLabels2,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=105)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartChannel2.png', transparent = True)

#-----------------------------------------------------------------------------------------------------------
# pie chart frequency of % change by pixel
statPixelList2 = []
for x in sumPixels2:
    if x == 0:
        statPixelList2.append(x)
    else:
        xx = round(((x/765) * 100), 0)
        statPixelList2.append(xx)
statPixelList2.sort()
lStatPixelList2 = len(statPixelList2)
# print('lStatPixelList1: ' + str(lStatPixelList1))

sTotal = 0
# More 0 here because zPixel is only 0 and these can round to 0.
for x in range(0,101):
    if statPixelList2.count(x)>0:
        #print('pixel count of ' + str(x) + ': ' + str(statPixelList2.count(x)))
        xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
        #print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
#print(sTotal)

r914 = 0
for x in range(9, 14):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r914 = r914 + xx
#print('r914: ' + str(r914))

r1420 = 0
for x in range(14, 20):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r1420 = r1420 + xx
#print('r1420: ' + str(r1420))

r2021 = 0
for x in range(20, 21):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r2021 = r2021 + xx
#print('r2021: ' + str(r2021))

r2129 = 0
for x in range(21,29):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r2129 = r2129 + xx
#print('r2129: ' + str(r2129))

r2937 = 0
for x in range(29, 37):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r2937 = r2937 + xx
#print('r2937: ' + str(r2937))

r3744 = 0
for x in range(37, 44):
    xx = round((((statPixelList2.count(x))/lStatPixelList2) * 100),2)
    r3744 = r3744 + xx
#print('r3744: ' + str(r3744))

orderedPixelStatList2 = [3.54, 11.63, 47.02, 11.06, 13.94, 12.81]
pieLabels2 = ['9-13%','14-19%','20%','21-28%','29-36%','37-43%']
explodeTuple2 = (0.0, 0.0, 0.1, 0.0, 0.0, 0.0)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedPixelStatList2,
                explode = explodeTuple2,
                labels = pieLabels2,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=45)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartPixel2.png', transparent = True)


#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# img3 Analysis
pixels3 = list(img3.getdata())
lPixels3 = len(pixels3)
values3 = []
sumPixels3 = []
for x in pixels3:
    xx = sum(x)
    if xx == 153:
        count+=1
    else:
        sumPixels3.append(xx)
    if x[0] == 68 and x[1] == 1 and x[2] == 84:
        foo = 0
    else:    
        values3.append(x[0])
        values3.append(x[1])
        values3.append(x[2])
lValues3 = len(values3)

# % of non zero pixel
zPixel3 = 0
for x in pixels3:
    res = sum(x)
    if res == 153:
        zPixel3 += 1
nZPixel3 = lPixels3 - zPixel3
statNZPixel3 = round(((nZPixel3/lPixels3) * 100), 2)
print('statNZPixel3: ' + str(statNZPixel3))
# print('zPixel3: ' + str(zPixel3))   
# print('lPixels3: ' + str(lPixels3)) 

# % of non zero channel
zChannel3 = 0
for x in values3:
    if x == 0:
        zChannel3 +=1
nZChannel3 = lValues3 -zChannel3
statNZChannel3 = round(((nZChannel3/lValues3) * 100), 2)
print('statNZChannel3: ' + str(statNZChannel3))

# Biggest % change by channel
bigChannel3 = 0
for x in values3:
    if x > bigChannel3:
        bigChannel3 = x
print('bigChannel3: ' + str(bigChannel3))
statChannel3 = round(((bigChannel3/255) * 100), 2)
print('statChannel3: ' + str(statChannel3))

# Biggest % change in a sumpixel
bigPixel3 = 0
for x in sumPixels3:
    if x > bigPixel3:
        bigPixel3 = x
print('bigPixel3: ' + str(bigPixel3))
statPixel3 = round(((bigPixel3/765) * 100), 2)
print('statPixel3: ' + str(statPixel3))

# pie chart frequency of % change by channel
statChannelList3 = []
for x in values3:
    xx = round(((x/255) * 100), 0)
    statChannelList3.append(xx)
statChannelList3.sort()
lStatChannelList3 = len(statChannelList3)

sTotal= 0
for x in range(0,101):
    if statChannelList3.count(x)>0:
        xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
        #print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
#print(sTotal)

r01 = 0
for x in range(0,16):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r01 = r01 + xx
#print('r01: ' + str(r01))

r16 = 0
for x in range(16,31):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r16 = r16 + xx
#print('r16: ' + str(r16))

r626 = 0
for x in range(31,46):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r626 = r626 + xx
#print('r626: ' + str(r626))

r2651 = 0
for x in range(46,61):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r2651 = r2651 + xx
#print('r2651: ' + str(r2651))

r5176 = 0
for x in range(61,76):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r5176 = r5176 + xx
#print('r5176: ' + str(r5176))

r76101 = 0
for x in range(76,92):
    xx = round((((statChannelList3.count(x))/lStatChannelList3) * 100),2)
    r76101 = r76101 + xx
#print('r76101: ' + str(r76101))

orderedChannelStatList3 = [16.82, 10.32, 19.64, 44.36, 4.24, 4.62]
pieLabels3 = ['0-15','16-30%','31-45%','46-60%','61-75%','76-92%']
explodeTuple3 = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedChannelStatList3,
                explode = explodeTuple3,
                labels = pieLabels3,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=105)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartChannel3.png', transparent = True)

# pie chart frequency of % change by pixel
statPixelList3 = []
for x in sumPixels3:

    if x == 0:
        statPixelList3.append(x)
    else:
        xx = round(((x/765) * 100), 0)
        statPixelList3.append(xx)
statPixelList3.sort()
lStatPixelList3 = len(statPixelList3)
# print('lStatPixelList3: ' + str(lStatPixelList3))

sTotal = 0
# More 0 here because zPixel is only 0 and these can round to 0.
for x in range(0,101):
    if statPixelList3.count(x)>0:
        #print('pixel count of ' + str(x) + ': ' + str(statPixelList3.count(x)))
        xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
        #print(str(x) + ': ' + str( xx ))
        sTotal = sTotal + xx
#print(sTotal)

r914 = 0
for x in range(9, 16):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r914 = r914 + xx
#print('r914: ' + str(r914))

r1420 = 0
for x in range(16, 23):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r1420 = r1420 + xx
#print('r1420: ' + str(r1420))

r2021 = 0
for x in range(23, 30):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r2021 = r2021 + xx
#print('r2021: ' + str(r2021))

r2131 = 0
for x in range(30,37):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r2131 = r2131 + xx
#print('r2131: ' + str(r2131))

r3141 = 0
for x in range(37, 43):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r3141 = r3141 + xx
#print('r3141: ' + str(r3141))

r4153 = 0
for x in range(43, 53):
    xx = round((((statPixelList3.count(x))/lStatPixelList3) * 100),2)
    r4153 = r4153 + xx
#print('r4153: ' + str(r4153))

orderedPixelStatList3 = [15.76, 19.58, 20.17, 20.83, 23.51, 0.15]
pieLabels3 = ['9-15','16-22%','23-30%','30-37%','37-43%','43-53%']
explodeTuple3 = (0.0, 0.0, 0.0, 0.0, 0.0, 0.1)

figureObject, axesObject = plt.subplots()

patches, labels, pct_texts = axesObject.pie(orderedPixelStatList3,
                explode = explodeTuple3,
                labels = pieLabels3,
                autopct='%1.2f',
                rotatelabels=True,
                startangle=90)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
plt.axis('equal')
plt.tight_layout()
plt.savefig(dirname + '/' + 'pieChartPixel3.png', transparent = True)