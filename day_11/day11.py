with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [[int(x) for x in line.strip()] for line in puzzle_input]

# Parse the energy levels grid into a `coordinates: value` dictionary of the form
# `(x, y): value`, similarly to day 9.
energy_levels = {
    (x, y): value for x, row in enumerate(puzzle_input) for y, value in enumerate(row)
}

# Define neighboring element positions (including diagonals)
neighbor_positions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, 1),
    (1, -1),
]


def compute_flashes(energy_levels):
    # Alternative ways to do what this function does are as follows:
    # - Keep a list of coordinates that are flashing, pop one off
    #   and add its neighbots to the list until the list is empty
    #   (https://github.com/alexander-yu/adventofcode/blob/master/problems_2021/11.py)
    # - Use recursion to increment the energy levels of neighboring octopuses
    #   (https://github.com/jonathanpaulson/AdventOfCode/blob/master/2021/11.py)
    # - Implement BFS/DFS
    #   (https://github.com/pantaryl/adventofcode/blob/main/2021/src/day11.py)
    step_num_flashes = 0
    octopuses_flashing = True
    while octopuses_flashing:
        # Assume octopuses are no longer flashing flashing.
        octopuses_flashing = False
        for (x, y), value in energy_levels.items():
            if value > 9:
                # At least once octopus is flashing so the step is not yet complete.
                octopuses_flashing = True
                step_num_flashes += 1
                # Use the energy value of `-1` to keep track of octopuses that have
                # already flashed since an octopus can only flash once during a step,
                # according to the challenge.
                energy_levels[(x, y)] = -1
                # Increment each neighboring octopus by 1 if the neighboring position is
                # valid and if the octopus has not already flashed this step.
                for dx, dy in neighbor_positions:
                    try:
                        if energy_levels[(x + dx, y + dy)] != -1:
                            energy_levels[(x + dx, y + dy)] += 1
                    except KeyError:
                        pass
    return energy_levels, step_num_flashes


num_flashes = 0
step = 1
part1_solution = None
part2_solution = None
while True:
    # Increment all the values in the `energy_levels` grid/dictionary each step.
    energy_levels = {x: y + 1 for x, y in energy_levels.items()}
    # Check for flashes until all octopuses have an energy state <= 9.
    energy_levels, step_num_flashes = compute_flashes(energy_levels)
    # Keep a tally of the number of times an octopus flashed for part 1.
    num_flashes += step_num_flashes
    # `-1` is a temporary value used to ensure octopuses only flash once per step.Thus,
    # before the next step starts we need to set all the temporary `-1`s back to `0`s.
    energy_levels = {x: 0 if y == -1 else y for x, y in energy_levels.items()}

    if step == 100:
        part1_solution = num_flashes
        # Only stop iterating if we have a solution to both parts of the challenge.
        if part2_solution:
            break
    # If all the energy values are 0 then all of the octopuses flashed on this step.
    if all(x == 0 for x in energy_levels.values()):
        part2_solution = step
        # Only stop iterating if we have a solution to both parts of the challenge.
        if part1_solution:
            break

    step += 1

print(f"Part 1 Solution: {part1_solution}")
print(f"Part 2 Solution: {part2_solution}")
