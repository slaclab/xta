from matplotlib import pyplot as plt
from PIL import Image
import os

dirname = os.path.dirname(__file__)
img1 = Image.open(dirname + '/' + 'png.250.patientXtest.40cm.png.png.250.patientXtest.20cm.png.40cm.difference.png')

pixels = list(img1.getdata())

# print(pixels)
count = 0
highest = 0
values = []
for x in pixels:
    
    #print(x)
    #print(x[0])
    if x!= (0,0,0):
        count+= 1
    for y in x:
        values.append(y)
        if y > highest:
            highest = y

size = len(pixels)
diff = ( count / size ) * 100
print('highest is ' + str(highest) + ' and diff is ' + str(diff))
values.sort()
# print(values)
pp = plt.hist(values)
plt.savefig('test.png')

ff = []
summ=0.00
for x in range(0,46):
    ff.append((values.count(x))/len(values)*100)
print('0: ' + str(ff[0]))
print('1: ' + str(ff[1]))
print('2: ' + str(ff[2]))
print('3: ' + str(ff[3]))
for x in range(4, 7):
    print(x)
    summ += ff[x]
print('4-6: ' + str(summ))
summ=0
for x in range(7, 46):
    print(x)
    summ += ff[x]
print('7-45: ' + str(summ))
pieLabels = '0', '1', '2', '3', '4-6', '7-45' 
ratios = [55.99076666666667, 21.20906666666667, 10.446466666666666, 5.030566666666666, 5.4414, 1.881733333333333]
explodeTuple = [0.1, 0.0, 0.0, 0.0, 0.0, 0.0]
figureObject, axesObject = plt.subplots()
patches, labels, pct_texts = axesObject.pie(ratios, explode = explodeTuple, labels = pieLabels, autopct = '%1.2f', startangle=90, rotatelabels=True)
for label, pct_text in zip(labels, pct_texts):
    pct_text.set_rotation(label.get_rotation())
axesObject.axis('equal')
plt.savefig('testpie.png')