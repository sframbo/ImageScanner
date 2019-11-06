import matplotlib.pyplot as plt
import numpy as np

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

N = 8
allowed_colors = {'R': 'red', 'Y': 'yellow', 'G': 'green', 'B': 'blue', '.': 'black'}

# prepare some coordinates
x, y, z = np.indices((N, N, N))

space = []
for i in range(N):
    cube = (x < i+1) & (y < N) & (z < N)
    space.append(cube)
#
# # draw cuboids in the top left and bottom right corners, and a link between them
# cube1 = (x < 3) & (y < 3) & (z < 3)
# cube2 = (x >= 5) & (y >= 5) & (z >= 5)
# link = abs(x - y) + abs(y - z) + abs(z - x) <= 2
#
#
#
#
# # combine the objects into a single boolean array
# voxels = cube1 | cube2 | link

voxel = space[0] | space[1] | space[2]

# set the colors of each object
colors = np.empty(voxel.shape, dtype=object)
colors[0] = 'red'
colors[1] = 'blue'
colors[2] = 'red'
# colors[link] = 'red'
# colors[cube1] = 'blue'
# colors[cube2] = 'green'

# and plot everything
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(space, facecolors=colors, edgecolor='k')

plt.show()