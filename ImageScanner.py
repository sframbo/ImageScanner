#!/usr/bin/env python3
from lib import *

print("Please enter input file location.")

# i = input()
i = "input.txt"

image_input = open(i)

# transform textfile into a 4x6 matrix
image_input = process_input(image_input)

print(image_input)

for (n, i) in image_input:
    calculate_weight(n, i)
