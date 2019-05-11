import os
import matplotlib.pyplot as pyplot
import matplotlib.image as image
from matplotlib.patches import Circle
import math
import time

# List all subdirectories
basepath = './'
catdirs = []
for entry in os.listdir(basepath):
    if os.path.isdir(os.path.join(basepath, entry)):
        catdirs.append('{0}{1}'.format(basepath, entry))

catimages = []
for dir in catdirs:
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file():
                filepath = '{0}/{1}'.format(dir, entry.name)
                filename, extension = os.path.splitext(filepath)
                if extension == '.jpg':
                    catimages.append(filepath)


for catimage in catimages:
    facefile = '{0}.face'.format(catimage)
    with open(facefile, 'r') as file:
        rawstring = file.read()

    intvalues = list(map(int, rawstring.split()))

    xvalues = (intvalues[0], intvalues[2], intvalues[6], intvalues[4], intvalues[0])
    yvalues = (intvalues[1], intvalues[3], intvalues[7], intvalues[5], intvalues[1])

    #figure, axis = pyplot.subplots(1)
    #img = image.imread(catimage)
    #axis.imshow(img)
    #axis.plot(xvalues, yvalues, linewidth=3, color='red')


    catfile = '{0}.cat'.format(catimage)
    with open(catfile, 'r') as file:
        rawstring = file.read()

    intvalues = list(map(int, rawstring.split()))

    num = intvalues.pop(0)
    xvalues = intvalues[0:][::2]
    yvalues = intvalues[1:][::2]

    markers = []

    #for i in range(0,num):
    #     markers.append(Circle((xvalues[i], yvalues[i]), radius=3, color='blue'))

    #for m in markers:
    #     axis.add_patch(m)

    minx = min(xvalues)
    miny = min(yvalues)
    maxx = max(xvalues)
    maxy = max(yvalues)

    paddingh = (maxx-minx)*0.1
    paddingv = (maxy-miny)*0.2

    x1 = minx-paddingh
    y1 = miny

    x2 = maxx+paddingh
    y2 = miny

    x3 = maxx+paddingh
    y3 = maxy+paddingv

    x4 = minx-paddingh
    y4 = maxy+paddingv

    xvalues = (x1, x2, x3, x4, x1)
    yvalues = (y1, y2, y3, y4, y1)

    filename = '{0}.bound'.format(catimage)
    facefile = open(filename, "w")
    facefile.write('{0} {1} {2} {3} {4} {5} {6} {7}'.format(
        int(x1),
        int(y1),
        int(x2),
        int(y2),
        int(x4),
        int(y4),
        int(x3),
        int(y3),
        )
    )
    facefile.close()

    #axis.plot(xvalues, yvalues, linewidth=3, color='red')
    #pyplot.show(figure)
