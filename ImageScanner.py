#!/usr/bin/env python3
from lib import process_input, calculate_weight, avg_all, avg_calc_vol, avg_elim_2, avg_elim_1, avg_cube_init


def image_scanner(interact=False, rotate=True, data="input.txt", timed=True, plot_=True, compared=False):
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

    # calculate the weight for each object in the file
    for (n, i) in image_input:
        calculate_weight(n, i, timed, plot_, _compare=compared)
        print()

    cube_init_avg = sum(avg_cube_init)/len(avg_cube_init)
    elim1_avg = sum(avg_elim_1)/len(avg_elim_1)
    elim2_avg = sum(avg_elim_2)/len(avg_elim_2)
    calc_vol_avg = sum(avg_calc_vol)/len(avg_calc_vol)
    overall_avg = sum(avg_all)/len(avg_all)

    print()
    print("---------- Average Time Analysis  -----------")
    print('Analyzed: {} objects'.format(len(avg_cube_init)))
    print('Cube Initialization: {0:.3f} ms'.format(cube_init_avg*1000))
    print('Check for void pixels: {0:.3f} ms'.format(elim1_avg*1000))
    print('Check for no match colors: {0:.3f} ms'.format(elim2_avg*1000))
    print('Calculate volume: {0:.3f} ms'.format(calc_vol_avg*1000))
    print('Overall: {0:.3f} ms'.format(overall_avg*1000))



