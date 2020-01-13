import numpy as np
from timeit import default_timer as timer
from Colors import translate_to, VOID, NO_COLOR
from Sides import FRONT, LEFT, BACK, RIGHT, TOP, BOTTOM
from Plotting import plot
import random

# TO DO:
# - create data type for color and transparent -- DONE
# - find a way to visually recreate the cube after algorithm -- DONE
# - add extra algorithm of checking if voxel is viewable and if not, then check from the opposite side. If at some point
#       a voxel is not viewable, assume the rest as not viewable . . R - - - L -- DONE


# this represents the 3-dimensional space containing the object
# each matrix represents a vertical slice of the space with the viewer observing it from the left of the container
cube_space = []
N = 0   # dimension
object_data = []    # image data of current object being processed
avg_cube_init = []
avg_elim_1 = []
avg_elim_2 = []
avg_calc_vol = []
avg_all = []

avg_cube_init_s = []
avg_elim_1_s = []
avg_elim_2_s = []
avg_calc_vol_s = []
avg_all_s = []

all_while_loops = []


def calculate_weight(_n, _i, _timed=True, _plt=True, _compare=False):
    global N
    global cube_space
    global object_data
    global avg_all
    global avg_calc_vol
    global avg_cube_init
    global avg_elim_1
    global avg_elim_2
    global all_while_loops

    runtime = 0
    N = _n
    # print("N changed to " + str(N))

    start = timer()
    initialize_cube_space(N)
    end = timer()
    length_1 = end - start

    runtime += length_1
    avg_cube_init.append(length_1/N)

    object_data = _i

    start = timer()
    is_empty_space = scan_for_see_through(_i)
    end = timer()
    length_2 = end - start
    runtime += length_2
    avg_elim_1.append(length_2/N)

    start = timer()
    if not is_empty_space:
        scan_for_no_match(_i)
    end = timer()
    length_3 = end - start
    runtime += length_3
    avg_elim_2.append(length_3/N)
    all_while_loops.append(while_loops)

    start = timer()
    print_max_weight(_empty=is_empty_space)
    end = timer()
    length_4 = end - start
    runtime += length_4
    avg_calc_vol.append(length_4/N)

    avg_all.append(runtime/N)
    # print(cube_space)

    print("Cubic dimension: {}x{}x{}".format(N, N, N))

    if _timed and _compare:
        runtime_s = 0
        start = timer()
        initialize_cube_space(N)
        end = timer()
        length_s1 = end - start
        runtime_s += length_s1
        avg_cube_init_s.append(length_s1 / N)

        object_data = _i

        start = timer()
        scan_for_see_through_slow(_i)
        end = timer()
        length_s2 = end - start
        runtime_s += length_s2
        avg_elim_1_s.append(length_s2 / N)

        start = timer()
        scan_for_no_match_slow(_i)
        end = timer()
        length_s3 = end - start
        runtime_s += length_s3
        avg_elim_2_s.append(length_s3 / N)

        start = timer()
        print_max_weight(True)
        end = timer()
        length_s4 = end - start
        runtime_s += length_s4
        avg_calc_vol_s.append(length_s4 / N)

        avg_all_s.append(runtime_s / N)

        print("☻ ---------- ANALYZING RUNTIME (per N) _ OPTIMIZED vs NAIVE ---------- ☻")
        print("While-loops: {}".format(while_loops))
        # print("Initialize cube elapse time: {0:.3f} ms vs {1:.3f} ms".format(length_1 * 1000, length_s1 * 1000))
        print("Scanning for void pixels: {0:.3f} ms vs {1:.3f} ms".format(length_2 * 1000, length_s2 * 1000))
        print("Scanning for match violations: {0:.3f} ms vs {1:.3f} ms".format(length_3 * 1000, length_s3 * 1000))
        # print("Calculating cubic volume: {0:.3f} ms vs {1:.3f} ms".format(length_4 * 1000, length_s4 * 1000))

        print("Overall Runtime per cube: {0:.3f} ms vs {1:.3f} ms".format(runtime * 1000, runtime_s * 1000))
        # print("Optimized version is {0:.3f} times faster than naive version.".format(runtime/runtime_s))
        print("------------------------------ ✂ ------------------------------")

    elif _timed:
        print("☻ -------- ANALYZING RUNTIME (per N) -------- ☻")
        print("While-loops: {}".format(while_loops))
        # print("Initialize cube elapse time: {0:.3f} ms".format(length_1 * 1000))
        print("Scanning for void pixels: {0:.3f} ms".format(length_2 * 1000))
        print("Scanning for match violations: {0:.3f} ms".format(length_3 * 1000))
        # print("Calculating cubic volume: {0:.3f} ms".format(length_4 * 1000))
        print("Overall Runtime per cube: {0:.3f} ms".format(runtime * 1000))
        print("----------------- ✂ -----------------")

    if _plt:
        plot(N, cube_space)


# sums up all the nonempty voxels in the 3d space
def print_max_weight(_print=True, _empty=False):
    total = 0
    if not _empty:
        for x in range(cube_space.shape[0]):
            for y in range(cube_space.shape[1]):
                for z in range(cube_space.shape[2]):
                    total = total + cube_space[x,y,z][0]
    if _print:
        print("Maximum weight: " + str(total) + " gram(s)")


def initialize_cube_space(N, w=1):
    global cube_space
    cube_space = np.empty((N,N,N), dtype=object)
    for a in range(cube_space.shape[0]):
        for b in range(cube_space.shape[1]):
            for c in range(cube_space.shape[2]):
                cube_space[a, b, c] = [w, "r"]


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
# NOTE: Only check FRONT, RIGHT and TOP sides as opposite sides mirror each other with regards to see-through pixels
def scan_for_see_through(image_input):
    # Locating the pixel marked with "." and delete all affected voxels
    redundant_sides = [BACK, LEFT, BOTTOM]
    for index, horizontal_slice in enumerate(image_input):
        for side, pixels in horizontal_slice.items():
            if side in redundant_sides:
                continue
            for pindex, pixel in enumerate(pixels):
                if pixel == VOID:
                    delete_nonexistent_voxels(index, side, pindex)
    return False


# read all sides
def scan_for_see_through_slow(image_input):
    # Locating the pixel marked with "." and delete all affected voxels
    for index, horizontal_slice in enumerate(image_input):
        for side, pixels in horizontal_slice.items():
            for pindex, pixel in enumerate(pixels):
                if pixel == VOID:
                    delete_nonexistent_voxels(index, side, pindex)
    return False


# delete all neighboring voxel from a given side + address
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


_offset = -1


def front_back_case(index, pindex, side):
    global cube_space
    pindex = N - pindex + _offset if side == BACK else pindex
    for p in range(N):
        cube_space[pindex][index][p][0] = 0


def right_left_case(index, pindex, side):
    global cube_space
    pindex = N - pindex + _offset if side == LEFT else pindex
    for p in range(N):
        cube_space[p][index][pindex][0] = 0


def top_bottom_case(index, pindex, side):
    global cube_space
    index = N - index + _offset if side == TOP else index
    for p in range(N):
        cube_space[pindex][p][index][0] = 0


# ======================================================================================
#            =========== SECOND ELIMINATION (THROUGH COMPARISON) ===========
# ======================================================================================
# this area is only executed when conceived space is detected as non-empty
_EMPTY = 0
_SOLID = 1
_current_is_viewable = False
while_loops = 0


# checking from all sides with while
def scan_for_no_match(inp):
    global while_loops
    overall_changed = True
    while_loops = 0
    while overall_changed:
        while_loops =+ 1
        overall_changed = False
        # front -> back
        global _current_is_viewable
        for X, vertical_slice in enumerate(cube_space):
            for Y, arr in enumerate(vertical_slice):
                for P, voxel in enumerate(arr):
                    if cube_space[X][Y][P][0] == _SOLID:
                        cube_space[X][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, P) else [_SOLID,
                                                                                                get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == _EMPTY else False
                        overall_changed = overall_changed or changed

                        ############# OPTIMIZING #############
                        if not _current_is_viewable:
                            reverse_check_2(X, Y, P, BACK)
                            break
                        _current_is_viewable = False
        # left -> right
        for P in range(0,N):
            for Y in range(0,N):
                for X in range(0,N):
                    if cube_space[X][Y][P][0] == _SOLID:
                        cube_space[X][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, P) else [_SOLID,
                                                                                                get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == _EMPTY else False
                        overall_changed = overall_changed or changed

                        ############# OPTIMIZING #############
                        if not _current_is_viewable:
                            reverse_check_2(X, Y, P, RIGHT)
                            break
                        _current_is_viewable = False
        # top -> bottom
        for P in range(0,N):
            for X in range(0,N):
                for Y in range(0,N):
                    if cube_space[X][Y][P][0] == _SOLID:
                        cube_space[X][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, P) else [_SOLID,
                                                                                                get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == _EMPTY else False
                        overall_changed = overall_changed or changed

                        ############# OPTIMIZING #############
                        if not _current_is_viewable:
                            reverse_check_2(X, Y, P, BOTTOM)
                            break
                        _current_is_viewable = False


def reverse_check_2(X, Y, P, side):
    global _current_is_viewable
    if side is BACK:
        for i in range(N - 1, P+1, -1):
            if cube_space[X][Y][i][0] == _SOLID:
                cube_space[X][Y][i] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, i) else [_SOLID, get_true_color(X, Y, i)]
                changed = True if cube_space[X][Y][i][0] == _EMPTY else False

                if not _current_is_viewable:
                    # print("not viewable. returning")
                    _current_is_viewable = False
                    return
                _current_is_viewable = False
    elif side is RIGHT:
        for i in range(N - 1, X+1, -1):
            if cube_space[i][Y][P][0] == _SOLID:
                cube_space[i][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(i, Y, P) else [_SOLID, get_true_color(i, Y, P)]
                changed = True if cube_space[i][Y][P][0] == _EMPTY else False
                if not _current_is_viewable:
                    # print("not viewable. returning")
                    _current_is_viewable = False
                    return
                _current_is_viewable = False
    elif side is BOTTOM:
        for i in range(N - 1, Y+1, -1):
            if cube_space[X][i][P][0] == _SOLID:
                cube_space[X][i][P] = [_EMPTY, NO_COLOR] if not is_solid(X, i, P) else [_SOLID, get_true_color(X, i, P)]
                changed = True if cube_space[X][i][P][0] == _EMPTY else False
                if not _current_is_viewable:
                    # print("not viewable. returning")
                    _current_is_viewable = False
                    return
                _current_is_viewable = False


# check from front and back with while-loop
def scan_for_no_match_(inp):
    global while_loops
    overall_changed = True
    while_loops = 0
    while overall_changed:
        while_loops += 1
        overall_changed = False
        for X, vertical_slice in enumerate(cube_space):
            for Y, arr in enumerate(vertical_slice):
                for P, voxel in enumerate(arr):

                    if cube_space[X][Y][P][0] == _SOLID:
                        cube_space[X][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, P) else [_SOLID,
                                                                                                get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == _EMPTY else False
                        overall_changed = overall_changed or changed

                        ############# OPTIMIZING #############
                        # IDEA: if current inspected pixel is not viewable from anywhere
                        #
                        global _current_is_viewable
                        if not _current_is_viewable:
                            reverse_check(X, Y, P)
                            _current_is_viewable = False
                            break
                        _current_is_viewable = False


def scan_for_no_match_slow(inp):
    overall_changed = True
    while overall_changed:
        overall_changed = False
        for X, vertical_slice in enumerate(cube_space):
            for Y, arr in enumerate(vertical_slice):
                for P, voxel in enumerate(arr):
                    # for each voxel, collect all color data from observable sides
                    if cube_space[X][Y][P][0] == _SOLID:
                        cube_space[X][Y][P] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, P) else [_SOLID,
                                                                                                get_true_color(X, Y, P)]
                        changed = True if cube_space[X][Y][P][0] == _EMPTY else False
                        overall_changed = overall_changed or changed


def reverse_check(X, Y, P):
    # print("p = {}".format(P))
    for i in range(N-1, P, -1):
        # print ("i = {}".format(i))
        if cube_space[X][Y][i][0] == _SOLID:
            cube_space[X][Y][i] = [_EMPTY, NO_COLOR] if not is_solid(X, Y, i) else [_SOLID, get_true_color(X, Y, i)]
            changed = True if cube_space[X][Y][i][0] == _EMPTY else False

            global _current_is_viewable
            if not _current_is_viewable:
                # print("not viewable. returning")
                _current_is_viewable = False
                return
            _current_is_viewable = False


# given location address of voxel, check if colors match from all viewable sides
def is_solid(X, Y, P):
    global _current_is_viewable
    colors = []
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]

    for side in sides:
        _is_viewable_from = is_viewable_from(side, X, Y, P)
        _current_is_viewable = _current_is_viewable or _is_viewable_from
        colors.append(get_color(side, X, Y, P).initial) if _is_viewable_from else ...
        if len(set(colors)) > 1: # check if more than one color is detected
            return False
    return True


def get_true_color(X, Y, P):
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]
    for side in sides:
        if is_viewable_from(side, X, Y, P):
            return get_color(side, X, Y, P).hex


def is_viewable(X, Y, P):
    sides = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT]
    viewable = False
    for side in sides:
        viewable = viewable or is_viewable_from(side, X, Y, P)
        if viewable:
            return True
    return False


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
