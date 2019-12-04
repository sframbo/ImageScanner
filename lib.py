import numpy as np
from Colors import translate_to, RED, GREEN, YELLOW, BLUE, CLEAR
from Sides import FRONT, LEFT, BACK, RIGHT, TOP, BOTTOM, translate_to_side


# TO DO:
# - create data type for color and transparent
# - find a way to visually recreate the cube after algorithm
# - add extra algorithm of checking if voxel is viewable and if not, then check from the opposite side. If at some point
#       a voxel is not viewable, assume the rest as not viewable . . R - - - L


# this represents the 3-dimensional space containing the object
# each matrix represents a vertical slice of the space with the viewer observing it from the left of the container
cube_space = [] # save color
N = 0   # dimension
object_data = []    # image data of current object being processed


def calculate_weight(n, i):
    global N
    global cube_space
    global object_data

    N = n
    cube_space = np.ones((N, N, N))
    object_data = i

    print("N changed to " + str(N))

    scan_for_see_through(i)
    scan_for_no_match(i)
    print_max_weight()
    print(cube_space)


# sums up all the nonempty voxels in the 3d space
def print_max_weight():
    print("Maximum Weight: " + str(np.sum(cube_space)) + " gram(s)")


def get_cube_space():
    return cube_space


def get_n():
    return N


def get_object_data():
    return object_data


# ===================================================================
#            =========== INPUT PROCESSING ===========
# ===================================================================
# accepts text file and returns a list of object data
def process_input(inp):
    #TO DO: prepare lines so that each data is translated into a certain datatype
    text_arr = inp.readlines()
    done = False
    index = 0
    n = int(text_arr[index])
    object_list = []

    while not done:
        image_data = prepare_object_data(n, index, text_arr)
        object_list.append((n, image_data))
        index = index + n + 1   # offset index to N of next data
        n = int(text_arr[index])
        done = True if n <= 0 else done

    return object_list


# accepts N:=dimension, offset in text and text input list. Returns array of dictionary containing horizontal slices
def prepare_object_data(n, offset, text_arr):
    object_data = []
    for i in range(n):
        horizontal_slice = prepare_slice(text_arr[offset+i+1])
        object_data.append(horizontal_slice)
    return object_data


# accepts a line from the text, splits by space and returns a horizontal slice (dict)
def prepare_slice(line):
    line = line.split()
    horizontal_slice = {
        FRONT:  process_line(line[0]),
        LEFT:   process_line(line[1]),
        BACK:   process_line(line[2]),
        RIGHT:  process_line(line[3]),
        TOP:    process_line(line[4]),
        BOTTOM: process_line(line[5])
    }
    return horizontal_slice


# accepts an array of strings returns an array of data type Color
def process_line(line):
    output = []
    for i in line:
        output.append(translate_to(i))
    return output


# not used. For reference only
def process_input_o(inp):
    global N
    global cube_space
    N = 3
    image_input_d = [
        {"front": ".R.", "left": "YYR", "back": ".Y.", "right": "RYY", "top": ".Y.", "bottom": ".R."},
        {"front": "GRB", "left": "YGR", "back": "BYG", "right": "RBY", "top": "GYB", "bottom": "GRB"},
        {"front": ".R.", "left": "YRR", "back": ".Y.", "right": "RRY", "top": ".R.", "bottom": ".Y."}
    ]
    cube_space = np.ones((N, N, N))
    return image_input_d


# ===================================================================
#            =========== FIRST ELIMINATION ===========
# ===================================================================
# Image input here is an array of slices in the form of dictionaries. Each dictionary containing pixel info on each side
# Locating the pixel marked with "." and delete all affected voxels
def scan_for_see_through(image_input):
    for index, horizontal_slice in enumerate(image_input):
        for side, pixels in horizontal_slice.items():
            for pindex, pixel in enumerate(pixels):
                if pixel == CLEAR:
                    delete_nonexistent_voxels(index, side, pindex)


# given location and side of voxel (maybe use a tupel?) delete depthwise all neighbors of that voxel
def delete_nonexistent_voxels(index, side, pindex):
    switch = {
        FRONT: lambda: front_back_case(index, pindex, FRONT),
        BACK: lambda: front_back_case(index, pindex, BACK),
        LEFT: lambda: right_left_case(index, pindex, LEFT),
        RIGHT: lambda: right_left_case(index, pindex, RIGHT),
        TOP: lambda: top_bottom_case(index, pindex, TOP),
        BOTTOM: lambda: top_bottom_case(index, pindex, BOTTOM)
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def front_back_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == BACK else pindex
    for p in range(N):
        cube_space[pindex][index][p] = 0
    # print(cube_space)


def right_left_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == LEFT else pindex
    for p in range(N):
        cube_space[p][index][pindex] = 0
    # print(cube_space)


def top_bottom_case(index, pindex, side):
    global cube_space
    index = N - index - 1 if side == TOP else index
    for p in range(N):
        cube_space[pindex][p][index] = 0


# ======================================================================================
#            =========== SECOND ELIMINATION (THROUGH COMPARISON) ===========
# ======================================================================================
# for reference only!
corners = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1)]

# this can still be optimized. Break if the previous voxel is inaccessible and then start from the opposite direction

# gegenbeispiel
# reihenfolge
# analyzes nonempty voxels in cube_space
# check if all accessible sides are same color. If no match, then set voxel to 0
def scan_for_no_match(inp):
    for X, vertical_slice in enumerate(cube_space):
        for Y, arr in enumerate(vertical_slice):
            for P, voxel in enumerate(arr):
                # collect all color data from observable sides
                if voxel == 1:
                    # if not is_accessible(X, Y, P):
                    #     break
                    cube_space[X][Y][P] = 0 if not is_solid(X, Y, P) else voxel


def is_accessible(X, Y, P):
    return True


# given location address of voxel, check if colors match from all viewable sides
def is_solid(X, Y, P):
    colors = []
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]

    for side in sides:
        colors.append(get_color(side, X, Y, P).initial) if is_viewable(side, X, Y, P) else nothing()
        if len(set(colors)) > 1: # check if more than one color is detected
            return False
    return True


def is_viewable(side, X, Y, P):
    switch = {
        FRONT: lambda: is_front_back_viewable(X, Y, 0, P),
        BACK: lambda: is_front_back_viewable(X, Y, P+1, N),
        LEFT: lambda: is_left_right_viewable(Y, P, 0, X),
        RIGHT: lambda: is_left_right_viewable(Y, P, X+1, N),
        TOP: lambda: is_top_bottom_viewable(X, P, 0, Y),
        BOTTOM: lambda: is_top_bottom_viewable(X, P, Y+1, N),
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def nothing():
    pass


def get_color(side, X, Y, P):
    offset = -1
    switch = {
        FRONT: lambda:   object_data[Y][FRONT][X],
        BACK: lambda:     object_data[Y][BACK][N-X+offset],
        LEFT: lambda:     object_data[Y][LEFT][N-P+offset],
        RIGHT: lambda:    object_data[Y][RIGHT][P],
        TOP: lambda:      object_data[N-P+offset][TOP][X],
        BOTTOM: lambda:   object_data[P][BOTTOM][X],
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def is_front_back_viewable(X, Y, start, end):
    ans = True
    for i in range(start, end):
        if cube_space[X][Y][i] == 1:
            ans = False
            break
    return ans


def is_top_bottom_viewable(X, P, start, end):
    ans = True
    for i in range(start, end):
        if cube_space[X][i][P] == 1:
            ans = False
            break
    return ans


def is_left_right_viewable(Y, P, start, end):
    ans = True
    for i in range(start, end):
        if cube_space[i][Y][P] == 1:
            ans = False
            break
    return ans


def compare_corners():
    corners_new = corners.copy()
    for i, t in enumerate(corners_new):
        corners_new[i] = tuple((N-1) * x for x in t)

    for (X, Y, Z) in corners_new:
        print(X, Y, Z)



