import numpy as np

# this represents the 3-dimensional space containing the object
# each matrix represents a vertical slice of the space with the viewer observing it from the left of the container
cube_space = []
N = 0


def get_cube_space():
    return cube_space


def get_n():
    return N


def calculate_weight(n, i):
    global N
    global cube_space

    N = n
    cube_space = np.ones((N, N, N))

    scan_for_see_through(i)
    scan_for_no_match(i)
    print_max_weight()


# sums up all the nonempty voxels in the 3d space
def print_max_weight():
    print("Maximum Weight: " + str(np.sum(cube_space)) + " gram(s)")


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
def scan_for_see_through(image_input):
    # Locating the pixel marked with "." and delete all affected voxels
    for index, horizontal_slice in enumerate(image_input):
        for side, pixels in horizontal_slice.items():
            for pindex, pixel in enumerate(pixels):
                if pixel == ".":
                    # print ("At slice " + str(index) + " Found see through pixel in " + side + " -> " + pixels + " at " + str(pindex))
                    # print("Value to be given: " + str(index) + " " + side + " " + str(pindex))
                    delete_nonexistent_voxel(index, side, pindex)


def front_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[pindex][index][p] = 0
    # print(cube_space)


def back_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[N - pindex - 1][index][p] = 0
    # print(cube_space)


def left_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[p][index][N - pindex - 1] = 0
    # print(cube_space)


def right_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[p][index][pindex] = 0
    # print(cube_space)


def top_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[pindex][p][N - index - 1] = 0
    # print(cube_space)


def bottom_case(index, pindex):
    global cube_space
    for p in range(N):
        cube_space[pindex][p][index] = 0
    # print(cube_space)


# given location and side of voxel (maybe use a tupel?) delete depthwise all neighbors of that voxel
def delete_nonexistent_voxel(index, side, pindex):
    switch = {
        "front": lambda: front_case(index, pindex),
        "back": lambda: back_case(index, pindex),
        "left": lambda: left_case(index, pindex),
        "right": lambda: right_case(index, pindex),
        "top": lambda: top_case(index, pindex),
        "bottom": lambda: bottom_case(index, pindex),
    }
    func = switch.get(side, lambda: "invalid")
    return func()


# ======================================================================================
#            =========== SECOND ELIMINATION (THROUGH COMPARISON) ===========
# ======================================================================================
# analyzes nonempty voxels in cube_space
# check if all accessible sides are same color. If no match, then set voxel to 0
def scan_for_no_match(inp):
    return 0

