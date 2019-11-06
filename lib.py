import numpy as np

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
        "front" : line[0],
        "left"  : line[1],
        "back"  : line[2],
        "right" : line[3],
        "top"   : line[4],
        "bottom": line[5]
    }
    return horizontal_slice


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
                if pixel == ".":
                    delete_nonexistent_voxels(index, side, pindex)


# given location and side of voxel (maybe use a tupel?) delete depthwise all neighbors of that voxel
def delete_nonexistent_voxels(index, side, pindex):
    switch = {
        "front": lambda: front_back_case(index, pindex, "front"),
        "back": lambda: front_back_case(index, pindex, "back"),
        "left": lambda: right_left_case(index, pindex, "left"),
        "right": lambda: right_left_case(index, pindex, "right"),
        "top": lambda: top_bottom_case(index, pindex, "top"),
        "bottom": lambda: top_bottom_case(index, pindex, "bottom")
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def front_back_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == "back" else pindex
    for p in range(N):
        cube_space[pindex][index][p] = 0
    # print(cube_space)


def right_left_case(index, pindex, side):
    global cube_space
    pindex = N - pindex -1 if side == "left" else pindex
    for p in range(N):
        cube_space[p][index][pindex] = 0
    # print(cube_space)


def top_bottom_case(index, pindex, side):
    global cube_space
    index = N - index - 1 if side == "top" else index
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
    sides = ["top", "bottom", "front", "back", "left", "right"]

    for side in sides:
        colors.append(get_color(side, X, Y, P)) if is_viewable(side, X, Y, P) else nothing()
        if len(set(colors)) > 1: # check if more than one color is detected
            return False
    return True


def is_viewable(side, X, Y, P):
    switch = {
        "front": lambda: is_front_back_viewable(X, Y, 0, P),
        "back": lambda: is_front_back_viewable(X, Y, P+1, N),
        "left": lambda: is_left_right_viewable(Y, P, 0, X),
        "right": lambda: is_left_right_viewable(Y, P, X+1, N),
        "top": lambda: is_top_bottom_viewable(X, P, 0, Y),
        "bottom": lambda: is_top_bottom_viewable(X, P, Y+1, N),
    }
    func = switch.get(side, lambda: "invalid")
    return func()


def nothing():
    pass


def get_color(side, X, Y, P):
    offset = -1
    switch = {
        "front": lambda : object_data[Y]["front"][X],
        "back": lambda: object_data[Y]["back"][N-X+offset],
        "left": lambda: object_data[Y]["left"][N-P+offset],
        "right": lambda: object_data[Y]["right"][P],
        "top": lambda: object_data[N-P+offset]["top"][X],
        "bottom": lambda: object_data[P]["bottom"][X],
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



