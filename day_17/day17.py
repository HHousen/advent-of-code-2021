# Amazing Walkthrough: https://github.com/mebeim/aoc/blob/master/2021/README.md#day-17---trick-shot

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

# Parse the `puzzle_input` and get the x and y coordinates.
target_x_coords, target_y_coords = puzzle_input.split(", y=")
target_y_coords = [int(x) for x in target_y_coords.split("..")]
target_x_coords = [int(x) for x in target_x_coords.split(": x=")[1].split("..")]

min_target_y_coord = min(target_y_coords)
# Find highest possible y position using math. The highest y position will be reached
# using a launch velocity such that the probe reaches `y = 0` at `n - 1` and
# `y = min_target_y_coord` at `n`, where `n` is the current step. Thus, the highest
# point is the sum from 1 to `(-min_target_y_coord - 1)`. As an equation, this is
# `highest_y_position = -min_target_y_coord * ((-min_target_y_coord - 1) // 2)`, which
# can be simplified as shown below.
highest_y_position = (min_target_y_coord) * (min_target_y_coord + 1) // 2

print(f"Part 1 Solution: {highest_y_position}")

# Make sure that `x1`/`y1` are always the smaller x/y coordinate and `x2`/`y2` are
# the larger x/y coodinate.
x1, x2, y1, y2 = (
    min(target_x_coords),
    max(target_x_coords),
    min(target_y_coords),
    max(target_y_coords),
)


def check_velocities(x_velocity, y_velocity, x_position=0, y_position=0):
    while True:
        # If the position of the probe is past the y lower bound or x upper bound of
        # the target then the probe has missed.
        if x_position > x2 or y_position < y1:
            return 0
        # If the position of the probe is past the minimum x coordinate and less than
        # the maximum y coordinate and the previous if statement fails, then the probe
        # is in the target area.
        elif x_position >= x1 and y_position <= y2:
            return 1
        # If none of the above are true, then we perform another step of the probe's
        # movement as per the challenge description.
        else:
            # The following two lines are performed first because they rely on the
            # velocity values, which are modified in place in two lines that follow.
            x_position += x_velocity
            y_position += y_velocity
            x_velocity -= x_velocity > 0
            y_velocity -= 1


hits = []
# Check `x_velocity` from 1 to `x2` (maximum x coordinate) inclusive. If the
# `x_velocity` is larger than `x2` then the probe will overshoot after the first step.
for x_velocity in range(1, x2 + 1):
    # Check `y_velocity` from `y1` (minimum y coodinate) to `-y1`. A `y_velocity` less
    # than `y1` will miss after one step. A `y_velocity` higher than the lowest y
    # coordinate will miss the target because launching the probe up with velocity `y`
    # means it will down with velocity `-y`.
    for y_velocity in range(y1, -y1):
        # For each potential initial velocity, check if it results in a hit.
        hits.append(check_velocities(x_velocity, y_velocity))

# Count the number of velocity combinations that were hits.
num_valid_initial_velocities = sum(hits)
print(f"Part 2 Solution: {num_valid_initial_velocities}")
