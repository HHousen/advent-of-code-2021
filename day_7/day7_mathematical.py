# This is a mathematical approach to Advent of Code 2021 Day 7 using median and mean.

import numpy as np

with open("puzzle_input.txt", "r") as file:
    crab_positions = np.fromfile(file, int, sep=",")


def fuel_modifier(fuel_amount):
    return fuel_amount * (fuel_amount + 1) // 2


part1_solution = sum(abs(crab_positions - np.median(crab_positions)))
print(f"Part 1 Solution {int(part1_solution)}")

part2_solution = sum(fuel_modifier(abs(crab_positions - int(crab_positions.mean()))))
print(f"Part 2 Solution: {part2_solution}")
