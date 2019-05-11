import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

im = np.array(Image.open('./CAT_01/00001394_026.jpg'), dtype=np.uint8)
f= open("./CAT_01/00001394_026.jpg.bound","r")

line_str = f.read()

i = 0;
coordinates = np.array([0, 0, 0, 0, 0, 0, 0, 0])
print(line_str)
numbers = line_str.split(' ')
for number in numbers:
    print(number)
    coordinates[i] = (int(number))
    i = i + 1

print(coordinates)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((coordinates[0], coordinates[1]),
                         coordinates[6] - coordinates[0],
                         coordinates[7] - coordinates[1],
                         linewidth=1,edgecolor='r',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()