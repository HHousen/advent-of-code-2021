from collections import defaultdict

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [
        [[int(y) for y in x.split(",")] for x in line.strip().split(" -> ")]
        for line in puzzle_input
    ]


def solve(puzzle_input, count_diagonals=False):
    points = defaultdict(int)
    for line in puzzle_input:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]

        if (x1 == x2 or y1 == y2) or count_diagonals:
            # Increment x/y if destination x/y is greater than starting x/y,
            # otherwise decrement.
            change_x = 1 if x2 > x1 else -1
            change_y = 1 if y2 > y1 else -1
            # Do not change the x/y coordinate if the starting x/y equals the
            # destination x/y.
            if x1 == x2:
                change_x = 0
            if y1 == y2:
                change_y = 0
            points[(x1, y1)] += 1
            # Keep adding coordinates until our current x and y equal the destination
            # x and y (`x1 == x2 and y1 == y2`).
            while not (x1 == x2 and y1 == y2):
                x1 += change_x
                y1 += change_y
                points[(x1, y1)] += 1
    # The score is the number of points that are crossed greater than or equal to two times.
    return sum(1 for v in points.values() if v >= 2)


part1_solution = solve(puzzle_input, count_diagonals=False)
print(f"Part 1 Solution: {part1_solution}")

part2_solution = solve(puzzle_input, count_diagonals=True)
print(f"Part 1 Solution: {part2_solution}")
