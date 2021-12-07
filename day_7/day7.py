with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

initial_crab_positions = [int(x) for x in puzzle_input.split(",")]

part1_fuel_amounts = []
part2_fuel_amounts = []


def fuel_modifier(fuel_amount):
    return fuel_amount * (fuel_amount + 1) // 2


# Loop through all possible alignment positions
for align_position in range(
    min(initial_crab_positions), max(initial_crab_positions) + 1
):
    # The amount of fuel used in part 1 is the sum for all crabs of the absolute
    # value of the difference between the desired alignment position and the crab's
    # initial position.
    part1_fuel_spent = sum(
        abs(align_position - crab_position) for crab_position in initial_crab_positions
    )
    # The amount of fuel used in part 2 is the sum for all crabs of the range from 1
    # to `abs(align_position - crab_position)` (inclusive). You can write this in
    # explicit Python like so: `sum(range(1, abs(align_position - crab_position) + 1)`,
    # but using the `fuel_modifier` function is faster.
    part2_fuel_spent = sum(
        fuel_modifier(abs(align_position - crab_position))
        for crab_position in initial_crab_positions
    )
    part1_fuel_amounts.append(part1_fuel_spent)
    part2_fuel_amounts.append(part2_fuel_spent)

# The solution is the amount of fuel needed for the optimal alignment position.
print(f"Part 1 Solution: {min(part1_fuel_amounts)}")
print(f"Part 2 Solution: {min(part2_fuel_amounts)}")
