from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import lib

mpl.rcParams['toolbar'] = 'None'
plt.style.use('dark_background')


def cuboid_data(pos, size=(1,1,1)):
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


def plot_cube_at(pos=(0, 0, 0), ax=None, c='b'):
    if ax is not None:
        X, Y, Z = cuboid_data(pos)
    ax.plot_surface(X, Y, Z, color=c, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False, alpha=1)


def plot_matrix_t(ax, matrix):
    # plot a Matrix
    for X, i in enumerate(matrix):
        for Y,  j in enumerate(i):
            for Z, k in enumerate(j):
                if k == 1:
                    # to have the
                    plot_cube_at(pos=(X, Y, Z), ax=ax)


def plot_matrix(ax, matrix):
    # plot a Matrix
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            for k in range(matrix.shape[2]):
                if matrix[i,j,k][0] is 1 and lib.is_viewable(i,j,k):
                    c = matrix[i,j,k][1]
                    plot_cube_at(pos=(i - 0.5, j - 0.5, k - 0.5), ax=ax, c=c)


def plot(N, ma, _rotate=False):
    fig = plt.figure('Object Scanner')

    ax = fig.gca(projection='3d')
    ax.axis('off')
    plot_matrix(ax, ma)

    if _rotate:
        while plt.fignum_exists(fig.number):
            for angle in range(0, 360):
                if not plt.fignum_exists(fig.number):
                    break
                ax.view_init(30, angle)
                plt.draw()
                plt.pause(.001)
            plt.close()
    else:
        while plt.fignum_exists(fig.number):
            for angle in range(0, 360):
                if not plt.fignum_exists(fig.number):
                    break
                plt.draw()
                plt.pause(.001)


def plot_1(N, ma):
    fig = plt.figure('Object Scanner')

    ax = fig.gca(projection='3d')
    ax.axis('off')
    plot_matrix(ax, ma)
    plt.draw()
    plt.pause(.001)
    return fig, ax


def update_plt(ax, ma, delay=.01):
    plt.cla()
    ax.axis('off')
    plot_matrix(ax, ma)
    plt.draw()
    plt.pause(delay)
