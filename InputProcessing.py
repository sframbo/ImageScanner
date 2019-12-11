# from Colors import translate_to, RED, GREEN, YELLOW, BLUE, CLEAR, UNKNOWN
# from Sides import FRONT, LEFT, BACK, RIGHT, TOP, BOTTOM, translate_to_side
# from lib import cube_space, N, object_data
#
# # ===================================================================
# #            =========== INPUT PROCESSING ===========
# # ===================================================================
# # accepts text file and returns a list of object data
# def process_input(inp):
#     text_arr = inp.readlines()
#     done = False
#     index = 0
#     n = int(text_arr[index])
#     object_list = []
#
#     while not done:
#         image_data = prepare_object_data(n, index, text_arr)
#         object_list.append((n, image_data))
#         index = index + n + 1   # offset index to N of next data
#         n = int(text_arr[index])
#         done = True if n <= 0 else done
#
#     return object_list
#
#
# # accepts N:=dimension, offset in text and text input list. Returns array of dictionary containing horizontal slices
# def prepare_object_data(n, offset, text_arr):
#     obj_d = []
#     for i in range(n):
#         horizontal_slice = prepare_slice(text_arr[offset+i+1])
#         obj_d.append(horizontal_slice)
#     return obj_d
#
#
# # accepts a line from the text, splits by space and returns a horizontal slice (dict)
# def prepare_slice(line):
#     line = line.split()
#     horizontal_slice = {
#         FRONT:  process_line(line[0]),
#         LEFT:   process_line(line[1]),
#         BACK:   process_line(line[2]),
#         RIGHT:  process_line(line[3]),
#         TOP:    process_line(line[4]),
#         BOTTOM: process_line(line[5])
#     }
#     return horizontal_slice
#
#
# # accepts an array of strings returns an array of data type Color
# def process_line(line):
#     output = []
#     for i in line:
#         output.append(translate_to(i))
#     return output
#
#
# # not used. For reference only
# def process_input_o(inp):
#     global N
#     global cube_space
#     N = 3
#     image_input_d = [
#         {"front": ".R.", "left": "YYR", "back": ".Y.", "right": "RYY", "top": ".Y.", "bottom": ".R."},
#         {"front": "GRB", "left": "YGR", "back": "BYG", "right": "RBY", "top": "GYB", "bottom": "GRB"},
#         {"front": ".R.", "left": "YRR", "back": ".Y.", "right": "RRY", "top": ".R.", "bottom": ".Y."}
#     ]
#     cube_space = np.ones((N, N, N))
#     return image_input_d