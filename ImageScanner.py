#!/usr/bin/env python3
from lib import process_input, calculate_weight, avg_all, avg_calc_vol, avg_elim_2, avg_elim_1, avg_cube_init
from lib import  avg_cube_init_s, avg_elim_1_s, avg_elim_2_s, avg_calc_vol_s, avg_all_s, all_while_loops
# from lib import N


def image_scanner(interact=False, rotate=True, data="input.txt", timed=True, plot_=False, plot_f=True, compared=True, _print=True):
    if interact:
        print("Please enter input file location.")
        i = input()
    else:
        i = data

    try:
        image_input = open(i)
    except FileNotFoundError:
        print('File not found')
        return

    # transform text file into a 4x6 matrix
    image_input = process_input(image_input)
    N = 0

    # calculate the weight for each object in the file
    for (n, i) in image_input:
        N = calculate_weight(n, i, timed, _compare=compared, _rotate=rotate, _plt=plot_, _plt_f=plot_f, _print=_print)
        print()

    if compared and timed:
        cube_init_avg_s = sum(avg_cube_init_s) / len(avg_cube_init_s)
        elim1_avg_s = sum(avg_elim_1_s) / len(avg_elim_1_s)
        elim2_avg_s = sum(avg_elim_2_s) / len(avg_elim_2_s)
        calc_vol_avg_s = sum(avg_calc_vol_s) / len(avg_calc_vol_s)
        overall_avg_s = sum(avg_all_s) / len(avg_all_s)

        cube_init_avg = sum(avg_cube_init) / len(avg_cube_init)
        elim1_avg = sum(avg_elim_1) / len(avg_elim_1)
        elim2_avg = sum(avg_elim_2) / len(avg_elim_2)
        calc_vol_avg = sum(avg_calc_vol) / len(avg_calc_vol)
        overall_avg = sum(avg_all) / len(avg_all)
        while_avg = sum(all_while_loops) / len(all_while_loops)

        if True:
            print("---------- Average Time Analysis (per voxel) - Optimized vs Naive -----------")
            print('Analyzed: {} objects'.format(len(avg_cube_init)))
            print('Cube Initialization: {0:.5f} ms'.format((cube_init_avg + cube_init_avg_s)*1000/2))
            print('Check for void pixels: {0:.5f} ms vs {1:.5f} ms'.format(elim1_avg * 1000, elim1_avg_s * 1000))
            print('Check for no match colors: {0:.5f} ms vs {1:.5f} ms'.format(elim2_avg * 1000,  elim2_avg_s * 1000))
            print('While loop repeats per object: {}'.format(while_avg))
            print('Calculate volume: {0:.5f} ms '.format((calc_vol_avg + calc_vol_avg_s) * 1000/2))
            print('Overall: {0:.5f} ms vs {1:.5f} ms'.format(overall_avg * 1000, overall_avg_s * 1000))
            print("----------------- ✂ -----------------\n")
        else:
            print("---------- Run Time Analysis (per N) - Optimized vs Naive -----------")
            print('Analyzed: {} objects'.format(len(avg_cube_init)))
            print('Cube Initialization: {0:.5f} ms'.format((cube_init_avg + cube_init_avg_s)*1000/2))
            print('Check for void pixels: {0:.5f} ms vs {1:.5f} ms'.format(elim1_avg * 1000 * N, elim1_avg_s * 1000 * N))
            print('Check for no match colors: {0:.3f} ms vs {1:.3f} ms'.format(elim2_avg * 1000 * N, elim2_avg_s * 1000 * N))
            print('While loop repeats per object: {}'.format(while_avg))
            print('Calculate volume: {0:.3f} ms '.format((calc_vol_avg*N + calc_vol_avg_s*N) * 1000 / 2))
            print('Overall: {0:.3f} ms vs {1:.3f} ms'.format(overall_avg*N * 1000, overall_avg_s*N * 1000))
            print("----------------- ✂ -----------------\n")

    elif timed:
        cube_init_avg = sum(avg_cube_init) / len(avg_cube_init)
        elim1_avg = sum(avg_elim_1) / len(avg_elim_1)
        elim2_avg = sum(avg_elim_2) / len(avg_elim_2)
        calc_vol_avg = sum(avg_calc_vol) / len(avg_calc_vol)
        overall_avg = sum(avg_all) / len(avg_all)
        while_avg = sum(all_while_loops) / len(all_while_loops)

        print("---------- Average Time Analysis  -----------")
        print('Analyzed: {} objects'.format(len(avg_cube_init)))
        print('Cube Initialization: {0:.5f} ms'.format(cube_init_avg * 1000))
        print('Check for void pixels: {0:.5f} ms'.format(elim1_avg * 1000))
        print('Check for no match colors: {0:.5f} ms'.format(elim2_avg * 1000))
        print('While loop repeats per object: {}'.format(while_avg))
        print('Calculate volume: {0:.5f} ms'.format(calc_vol_avg * 1000))
        print('Overall: {0:.5f} ms'.format(overall_avg * 1000))
        print("----------------- ✂ -----------------\n")





