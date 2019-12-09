from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


def cuboid_data(pos, size=(1,1,1)):
    # code taken from
    # https://stackoverflow.com/a/35978146/4124317
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the (left, outside, bottom) point
    o = [a - b / 2 for a, b in zip(pos, size)]
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)


def plotCubeAt(pos=(0,0,0),ax=None, c='b'):
    # Plotting a cube element at position pos
    if ax !=None:
        X, Y, Z = cuboid_data( pos )
        ax.plot_surface(X, Y, Z, color=c, rstride=1, cstride=1, alpha=1)


def plotMatrix_T(ax, matrix):
    # plot a Matrix
    for X, i in enumerate(matrix):
        for Y,  j in enumerate(i):
            for Z, k in enumerate(j):
                if k == 1:
                    # to have the
                    plotCubeAt(pos=(X, Y, Z), ax=ax)


def plotMatrix(ax, matrix):
    # plot a Matrix
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for k in range(matrix.shape[2]):
                if matrix[i,j,k][0] == 1:
                    # to have the
                    c = matrix[i,j,k][1]
                    plotCubeAt(pos=(i-0.5,j-0.5,k-0.5), ax=ax, c=c)


def plot(N, ma):
    N1 = N
    N2 = N
    N3 = N
    # ma = np.random.choice([0, 1], size=(N1, N2, N3), p=[0.99, 0.01])


    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # ax.set_aspect('equal')

    plotMatrix(ax, ma)

    plt.show()

    print(ma)


ma = np.empty((2,2,2), dtype=object)
for a in range(ma.shape[0]):
    for b in range(ma.shape[1]):
        for c in range(ma.shape[2]):
            ma[a, b, c] = [1, "r"]

ma[0,0,0][1] = 'b'
ma[1,1,1][0] = 0

print(ma)

# plot(2, ma)