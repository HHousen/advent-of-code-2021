import math
from functools import reduce
from itertools import permutations

with open("puzzle_input.txt", "r") as puzzle_input:
    # Read the puzzle input by applying the `eval` function to each line of the
    # `puzzle_input`. This will create a list where each item is the Python object
    # representation (list of lists of lists etc) of the corresponding line of the
    # `puzzle_input`.
    puzzle_input = list(map(eval, puzzle_input.read().strip().splitlines()))


def add_right(number, left):
    if isinstance(number, int):
        return number + left
    return [number[0], add_right(number[1], left)]


def add_left(number, right):
    if isinstance(number, int):
        return number + right
    return [add_left(number[0], right), number[1]]


def explode(number, idx=4):
    # The return pattern for this function is as follows:
    # `change, number, left, right`.
    # If the `number` is an integer then return just the `number` because only pairs
    # can be exploded. "Exploding pairs will always consist of two regular numbers."
    if isinstance(number, int):
        return False, number, None, None
    # Separate the `number` into left and right portions.
    left_inner_number, right_inner_number = number
    # If the current depth into the nested list that represents a snailfish number is
    # 0, then we have reached a pair that is nested inside four pairs since `idx`
    # starts at 4. If this is the case, then a change should be made and the `explode`
    # action should run.
    if idx == 0:
        # We return `0` as the `new_number` because "the entire exploding pair is
        # replaced with the regular number 0" when a pair is marked to be exploded.
        return True, 0, left_inner_number, right_inner_number
    # `explode` the left side of the `number` first because only the leftmost nested
    # pair explodes if the conditions are met. Keep track of the current depth with the
    # `idx` variable. So, for each recursive call to `explode`, decrement the `idx`
    # by 1.
    change, new_number, new_left_inner_number, new_right_inner_number = explode(
        left_inner_number, idx=idx - 1
    )
    # If the `left_inner_number` should be exploded, then perform the explode action.
    # "The pair's left value is added to the first regular number to the left of the
    # exploding pair (if any), and the pair's right value is added to the first regular
    # number to the right of the exploding pair (if any)."
    if change:
        return (
            True,
            [new_number, add_left(right_inner_number, new_right_inner_number)],
            new_left_inner_number,
            0,
        )
    # Perform the same actions on the `right_inner_number` that we performed on the
    # `left_inner_number`.
    change, new_number, new_left_inner_number, new_right_inner_number = explode(
        right_inner_number, idx=idx - 1
    )
    if change:
        return (
            True,
            [add_right(left_inner_number, new_left_inner_number), new_number],
            0,
            new_right_inner_number,
        )
    # Return the `number` with no changes if all of the above logic is executed but
    # the conditions to perform the `explode` action are not met.
    return False, number, 0, 0


def split(number):
    if isinstance(number, int):
        # If the `number` is an integer and it is greater than or equal to 10, then
        # split the regular number by replacing "it with a pair; the left element of
        # the pair should be the regular number divided by two and rounded down, while
        # the right element of the pair should be the regular number divided by two and
        # rounded up."
        if number >= 10:
            return [math.floor(number / 2), math.ceil(number / 2)]
        # If the `number` is an integer but is less than 10, then simply return the
        # `number` since no modifications are necessary.
        return number
    # Separate the `number` to get the first and second halves.
    first_inner_number, second_inner_number = number
    # `split` the first half of the `number`. If the first half is an integer, then it
    # will be split appropriately and returned. If the first half is a list, then it
    # will be recursively split until individual numbers are reached.
    new_first_inner_number = split(first_inner_number)
    # If the splitted left number is not the same as the original left number, then
    # the left number was splitted and the new number will be returned.
    if new_first_inner_number != first_inner_number:
        return [new_first_inner_number, second_inner_number]
    # If nothing on the left side was `split` then the first standard integer greather
    # than or equal to 10 must be on the right side of the number. Recursively split
    # the right side exactly how the left side was split.
    new_second_inner_number = split(second_inner_number)
    # Finally, return the original left side number + the new right side number, no
    # matter if the right side number was modified or not (we check if it was modified
    # in the `add` function).
    return [first_inner_number, new_second_inner_number]


def add(first_number, second_number):
    # "To add two snailfish numbers, form a pair from the left and right parameters
    # of the addition operator." In other words, combine the two numbers that are being
    # added into a single list.
    number = [first_number, second_number]
    # Perform reduction if necessary until the number is reduced.
    while True:
        change, number, _, _ = explode(number)
        if change:
            # Keep performing the `explode` action until it doesn't result in a change
            # to the `number`.
            continue
        new_number = split(number)
        if new_number == number:
            # If the `explode` action did not make a change and the `split` action did
            # not make a change to the `number`, then the `number` is reduced so break
            # the reduction loop.
            break
        number = new_number
    return number


def magnitude(number):
    # "The magnitude of a regular number is just that number."
    if isinstance(number, int):
        return number
    # "The magnitude of a pair is 3 times the magnitude of its left element plus 2
    # times the magnitude of its right element."
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


# Apply the `add` function cumulatively to the `puzzle_input` in groups of two, from
# left to right, so as to reduce the `puzzle_input` to a single value by essentially
# adding all of the values together.
final_number = reduce(add, puzzle_input)
# Recursively calculate the magnitude of the final snailfish number sum according to
# the challenge description.
part1_solution = magnitude(final_number)
print(f"Part 1 Solution: {part1_solution}")

# For each permutation of two snailfish numbers in the `puzzle_input`, `add` them
# together, and calculate the magnitude of the sum. Then, find the maximum sum in
# this list.
largest_2_sum_magnitude = max(
    magnitude(add(a, b)) for a, b in permutations(puzzle_input, 2)
)
print(f"Part 2 Solution: {largest_2_sum_magnitude}")
