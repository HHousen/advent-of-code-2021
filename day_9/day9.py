import math
from collections import deque

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [[int(x) for x in line.strip()] for line in puzzle_input]

# Parse the height grid into a `coordinates: value` dictionary of the form
# `(x, y): value`.
heights = {
    (x, y): value for x, row in enumerate(puzzle_input) for y, value in enumerate(row)
}

# Define neighboring element positions
neighbor_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

minima = {}
for (x, y), value in heights.items():
    # Check if all neighboring element are less than the current value. For each
    # neighbor's position (dx, dy), modify the current value's position accordingly,
    # then, try to get the value at that position from the `heights` dictionary. If that
    # value cannot be found (it is an edge or corner), then return `math.inf` so the
    # current `value` is less than the nonexistant neighbor.
    if all(
        value < heights.get((x + dx, y + dy), math.inf) for dx, dy in neighbor_positions
    ):
        minima[(x, y)] = value

# The part 1 solution is the sum of all the `value + 1` at all the minimum point. This
# is the same as the sum of all the values and the sum of the length.
part1_solution = sum(minima.values()) + len(minima)
print(f"Part 1 Solution: {part1_solution}")


# Implementation of Breadth First Search (BFS) to find basins.
def bfs(graph, node):
    visited = set()
    # `deque` is "a list-like container with fast appends and pops on either end."
    queue = deque()
    visited.add(node)
    queue.append(node)

    while queue:
        # `queue` holds the key values from the `heights` dictionary.
        x, y = queue.popleft()

        # Define neighboring positions from the current position.
        neighbors = [(x + dx, y + dy) for dx, dy in neighbor_positions]
        for neighbor in neighbors:
            # Only check the neighbor is it hasn't been visited and if it is a valid
            # neighbor that is in the `graph`/`heights`.
            if neighbor not in visited and neighbor in graph:
                height = graph[neighbor]
                # A height of 9 cannot be included per challenge description.
                if height < 9:
                    visited.add(neighbor)
                    queue.append(neighbor)

    return visited


# Conduct a BFS on each minimum point in the `heights` grid. `bfs()` returns
# a list of coordinates that are part of the basin formed at `node`.
basins = [bfs(heights, node) for node in minima.keys()]
# Sort the basins by number of points, as per the challenge description.
basins_lengths = sorted(len(basin) for basin in basins)
# Multiple the lengths of the largest basins, which is the challenge answer.
part2_solution = math.prod(basins_lengths[-3:])

print(f"Part 2 Solution: {part2_solution}")
