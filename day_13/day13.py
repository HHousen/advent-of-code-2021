with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

# Split the input into the coordinates and flip instructions.
coords, flips = puzzle_input.split("\n\n")
# Parse the dot coordinates into a set of tuples in the form `(x, y)`.
dots = set((int(x) for x in line.split(",")) for line in coords.split("\n"))
# Parse the flips into a list of tuples in the form `(axis, position)`.
flips = [tuple(instruction.split()[-1].split("=")) for instruction in flips.split("\n")]

# Define variable to store the output of the first flip.
first_flip = None
# Perform the flip/reflection for each flip instruction.
for idx, flip_instruction in enumerate(flips):
    axis, position = flip_instruction
    position = int(position)

    # Define a new set to hold the output coordinates of this flip.
    new_dots = set()
    # Perform the fold for each dot.
    for x, y in dots:
        # We check if the `x`/`y` is greater than the axis to flip over because
        # points left/above the flip axis do not get moved. If we are flipping up along
        # a horizontal y axis then the x coordinate (the horizontal coordinate) doesn't
        # change, and vice versa for an x-axis.
        if axis == "y" and y > position:
            # Compute the new y coordinate by reflecting it over the corespdong y-axis.
            # Reflecting over *the* y-axis would simply be the negative of the current
            # y coordinate. Since we are using an arbitrary y-axis, we take the
            # negative of the coordinate and then add `2*axis_position` so that the
            # point is equidistant from the axis of reflection. This same logic applies
            # when the x-axis is the reflection axis.
            new_dots.add((x, 2 * position - y))
        elif axis == "x" and x > position:
            new_dots.add((2 * position - x, y))
        else:
            # If the coordinates are not in the region to be flipped, then simply add
            # them to the `new_dots` set.
            new_dots.add((x, y))

    dots = new_dots
    # If we just computed the first flip, then store the output so we can find the
    # answer to part 1 of the puzzle.
    if idx == 0:
        first_flip = new_dots

part1_solution = len(first_flip)
print(f"Part 1 Solution: {part1_solution}")


def print_grid(dots):
    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            # Print a "#" if the current coordinate is the position of a dot, otherwise
            # just display a space.
            print("#" if (x, y) in dots else " ", end="")
        print()  # Print a newline after each x-axis line
    print()  # Print a newline after the entire grid has been displayed


print("Part 2 Solution:")
print_grid(dots)
