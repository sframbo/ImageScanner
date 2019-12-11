import numpy as np
from timeit import default_timer as timer
from Colors import translate_to, VOID, CLEAR
from Sides import FRONT, LEFT, BACK, RIGHT, TOP, BOTTOM
from Plotting import plot

# TO DO:
# - create data type for color and transparent -- DONE
# - find a way to visually recreate the cube after algorithm -- DONE
# - add extra algorithm of checking if voxel is viewable and if not, then check from the opposite side. If at some point
#       a voxel is not viewable, assume the rest as not viewable . . R - - - L


# this represents the 3-dimensional space containing the object
# each matrix represents a vertical slice of the space with the viewer observing it from the left of the container
cube_space = [] # save color
N = 0   # dimension
object_data = []    # image data of current object being processed


def calculate_weight(n, i, timed=True):
    global N
    global cube_space
    global object_data
    runtime = 0
    N = n
    print("N changed to " + str(N))

    start = timer()
    initialize_cube_space(N)
    end = timer()
    if timed:
        print("#####################################################################")
        print("######################### RUN TIME ANALYSIS #########################")
        print("#####################################################################")
        print("Cubic dimension: {}x{}x{}".format(N, N, N))

        print("Initialize cube elapse time: {} seconds".format(end - start))
    runtime += end-start
    object_data = i

    start = timer()
    scan_for_see_through(i)
    end = timer()
    if timed:
        print("Scanning for void pixels: {} seconds".format(end - start))
    runtime += end-start

    start = timer()
    scan_for_no_match(i)
    end = timer()
    if timed:
        print("Scanning for match violations: {} seconds".format(end - start))
    runtime += end - start

    start = timer()
    print_max_weight()
    end = timer()
    if timed:
        print("Calculating cubic volume: {} seconds".format(end - start))
        print("#####################################################################")
        print("##########################       END        #########################")
        print("#####################################################################")
    runtime += end - start

    print("Runtime: {}".format(runtime))
    # print(cube_space)
    plot(N, cube_space)



# sums up all the nonempty voxels in the 3d space
def print_max_weight():
    total = 0
    for x in range(cube_space.shape[0]):
        for y in range(cube_space.shape[1]):
            for z in range(cube_space.shape[2]):
                total = total + cube_space[x,y,z][0]
    print("Maximum Weight: " + str(total) + " gram(s)")


def initialize_cube_space(N):
    global cube_space
    cube_space = np.empty((N,N,N), dtype=object)
    for a in range(cube_space.shape[0]):
        for b in range(cube_space.shape[1]):
            for c in range(cube_space.shape[2]):
                cube_space[a, b, c] = [1, "r"]


# ===================================================================
#            =========== INPUT PROCESSING ===========
# ===================================================================
# accepts text file and returns a list of object data
def process_input(inp):
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
    obj_d = []
    for i in range(n):
        horizontal_slice = prepare_slice(text_arr[offset+i+1])
        obj_d.append(horizontal_slice)
    return obj_d


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


# ===================================================================
#            =========== FIRST ELIMINATION ===========
# ===================================================================
# Image input here is an array of slices in the form of dictionaries. Each dictionary containing pixel info on each side
# Locating the pixel marked with "." and delete all affected voxels
def scan_for_see_through(image_input):
    for index, horizontal_slice in enumerate(image_input):
        for side, pixels in horizontal_slice.items():
            for pindex, pixel in enumerate(pixels):
                if pixel == VOID:
                    delete_nonexistent_voxels(index, side, pindex)


def delete_nonexistent_voxels(index, side, pindex):
    switch = {
        FRONT:  lambda: front_back_case(index, pindex, FRONT),
        BACK:   lambda: front_back_case(index, pindex, BACK),
        LEFT:   lambda: right_left_case(index, pindex, LEFT),
        RIGHT:  lambda: right_left_case(index, pindex, RIGHT),
        TOP:    lambda: top_bottom_case(index, pindex, TOP),
        BOTTOM: lambda: top_bottom_case(index, pindex, BOTTOM)
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def front_back_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == BACK else pindex
    for p in range(N):
        cube_space[pindex][index][p][0] = 0


def right_left_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == LEFT else pindex
    for p in range(N):
        cube_space[p][index][pindex][0] = 0


def top_bottom_case(index, pindex, side):
    global cube_space
    index = N - index - 1 if side == TOP else index
    for p in range(N):
        cube_space[pindex][p][index][0] = 0


# ======================================================================================
#            =========== SECOND ELIMINATION (THROUGH COMPARISON) ===========
# ======================================================================================
# this can still be optimized. Break if the previous voxel is inaccessible and then start from the opposite direction
# gegenbeispiel
# reihenfolge
# analyzes nonempty voxels in cube_space
# check if all accessible sides are same color. If no match, then set voxel to 0
# maybe repeat an iteration for as long as there are changes done in the last iteration? but do a localized search
# relative to location of the last changed voxel
def scan_for_no_match(inp):
    overall_changed = True
    while overall_changed:
        overall_changed = False
        for X, vertical_slice in enumerate(cube_space):
            for Y, arr in enumerate(vertical_slice):
                for P, voxel in enumerate(arr):
                    changed = False
                    # for each voxel, collect all color data from observable sides
                    if cube_space[X][Y][P][0] == 1:
                        cube_space[X][Y][P] = [0, CLEAR] if not is_solid(X, Y, P) else [1, get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == 0 else False
                        overall_changed = overall_changed or changed
                        if not changed:
                            reverse_check(X, Y, P)
                            continue

#                     if state remains to 1, break and reverse iteration (check from opposite direction)
#                 if change occurs, propagate to nearby neighbors?


def reverse_check(X, Y, P):
    i = N-1
    changed = False
    while i > P:
        if cube_space[X][Y][i][0] == 1:
            cube_space[X][Y][i] = [0, CLEAR] if not is_solid(X, Y, i) else [1, get_true_color(X, Y, i)]
            changed = True if cube_space[X][Y][i][0] == 0 else False
            if not changed:
                return
        i -= 1


# given location address of voxel, check if colors match from all viewable sides
def is_solid(X, Y, P):
    colors = []
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]

    for side in sides:
        colors.append(get_color(side, X, Y, P).initial) if is_viewable_from(side, X, Y, P) else nothing()
        if len(set(colors)) > 1: # check if more than one color is detected
            return False
    return True


def get_true_color(X, Y, P):
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]
    for side in sides:
        if is_viewable_from(side, X, Y, P):
            return get_color(side, X, Y, P).hex


def is_viewable_from(side, X, Y, P):
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


def is_viewable(X, Y, P):
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]
    viewable = False
    for side in sides:
        viewable = viewable or is_viewable_from(side, X, Y, P)
        if viewable:
            return True
    return False


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
        if cube_space[X][Y][i][0] == 1:
            ans = False
            break
    return ans


def is_top_bottom_viewable(X, P, start, end):
    ans = True
    for i in range(start, end):
        if cube_space[X][i][P][0] == 1:
            ans = False
            break
    return ans


def is_left_right_viewable(Y, P, start, end):
    ans = True
    for i in range(start, end):
        if cube_space[i][Y][P][0] == 1:
            ans = False
            break
    return ans

#