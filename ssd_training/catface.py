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
    catfile = '{0}.cat'.format(catimage)
    with open(catfile, 'r') as file:
        rawstring = file.read()

    intvalues = list(map(int, rawstring.split()))

    num = intvalues.pop(0)
    xvalues = intvalues[0:][::2]
    yvalues = intvalues[1:][::2]

    poes = (2, 4, 7)

    a = yvalues[poes[1]] - yvalues[poes[2]]
    b = xvalues[poes[2]] - xvalues[poes[1]]
    c = xvalues[poes[1]]*yvalues[poes[2]] - xvalues[poes[2]]*yvalues[poes[1]]

    d = (a*xvalues[poes[0]] + b*yvalues[poes[0]] + c)/math.sqrt(a**2 + b**2)

    height = d*1.1

    AC = xvalues[poes[2]] - xvalues[poes[1]]
    BC = yvalues[poes[2]] - yvalues[poes[1]]

    if abs(AC) < 1:
        AC = 0.01
    alpha = -math.atan(BC/AC)

    x1 = xvalues[poes[1]] + height*math.sin(alpha)
    y1 = yvalues[poes[1]] + height*math.cos(alpha)
    x2 = xvalues[poes[2]] + height*math.sin(alpha)
    y2 = yvalues[poes[2]] + height*math.cos(alpha)

    filename = '{0}.face'.format(catimage)
    facefile = open(filename, "w")
    facefile.write('{0} {1} {2} {3} {4} {5} {6} {7}'.format(
        int(xvalues[poes[1]]),
        int(yvalues[poes[1]]),
        int(xvalues[poes[2]]),
        int(yvalues[poes[2]]),
        int(x1),
        int(y1),
        int(x2),
        int(y2))
    )
    facefile.close()

    # markers = []
    #
    # markers.append(Circle((x1, y1), radius=3, color='blue'))
    # markers.append(Circle((x2, y2), radius=3, color='blue'))
    #
    # for i in poes:
    #     markers.append(Circle((xvalues[i], yvalues[i]), radius=3, color='red'))
    #
    # figure, axis = pyplot.subplots(1)
    # img = image.imread(catimage)
    # axis.imshow(img)
    # for m in markers:
    #     axis.add_patch(m)
    # pyplot.show(figure)
