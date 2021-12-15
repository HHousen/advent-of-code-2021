# This code is inspired by this walkthrough:
# https://github.com/mebeim/aoc/blob/master/2021/README.md#day-15---chiton

from collections import defaultdict
from queue import PriorityQueue

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [[int(x) for x in line.strip()] for line in puzzle_input]


def neighbors_non_diagonal(x, y, height, width):
    # Get the coordinates of neighboring items in the grid that are not diagonally
    # adjacent.
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = (x + dx, y + dy)
        if 0 <= new_x < width and 0 <= new_y < height:
            yield new_x, new_y


# Implementation of Dijkstra's algorithm to find the least-cost path from `source` to
# `destination`. More info here: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm.
# Here is a guide that explains how Dijkstra's algorithm works for graphs:
# https://stackabuse.com/dijkstras-algorithm-in-python/.
def dijkstra(grid, source=(0, 0), destination=None):
    grid_height, grid_width = len(grid), len(grid[0])
    if not destination:
        destination = (grid_height - 1, grid_width - 1)

    # Difference between `Queue.PriorityQueue` and a `heapq`:
    # https://stackoverflow.com/a/36991722. PriorityQueue uses `heapq` internally.
    queue = PriorityQueue()
    # Start with only the source in the `queue` and in the `min_costs` dictionary.
    # The source has a distance of 0.
    queue.put((0, source))
    min_costs = defaultdict(lambda: float("inf"))
    min_costs[source] = 0
    visited = set()

    while not queue.empty():
        # Get the node with the lowest cost/distance from the `source` node.
        distance, node = queue.get()

        # If the node with the shortest distance is the `destination` node,
        # then we have the answer (the total distance/cost from the `source` node
        # to the `destination` node).
        if node == destination:
            return distance

        # If the node has already been visited, then skip it and test the next node.
        if node in visited:
            continue

        # We have now visited this node so we will add it to the visited set.
        visited.add(node)
        x, y = node

        # for each neighboring (non diagonal) node...
        for neighbor in neighbors_non_diagonal(x, y, grid_height, grid_width):
            # If this neighbor has already been visited, then skip it and try the next
            # neighbor.
            if neighbor in visited:
                continue

            new_x, new_y = neighbor
            # The `new_cost` is the total distance from the `source` to this neighbor.
            new_cost = distance + grid[new_x][new_y]
            old_cost = min_costs[neighbor]

            # If the `new_cost` is less than the previous minimum cost to reach this
            # neighbor, then update the neighbor's minimum cost to the `new_cost`.
            # Add this distance and neighbor to the queue since we have found a better
            # path.
            if new_cost < old_cost:
                min_costs[neighbor] = new_cost
                queue.put((new_cost, neighbor))

    # Return infinity if there is no path from the `source` to the `destination`.
    return float("inf")


# We can think of the `puzzle_input` grid as a directed graph with the number of nodes
# equal to the number of items in the grid. The edges of the graph are the values of
# the adjacent items. For example, moving from position A to position B in the grid
# represents two nodes on the graph and the edge is the risk level of B. Moving from
# B to A costs the value at position A. The edges going to a node have the same weight
# as the risk level of that node.
part1_min_risk = dijkstra(puzzle_input)

print(f"Part 1 Solution: {part1_min_risk}")


def expand_grid(grid):
    original_tile_width = len(grid)
    original_tile_height = len(grid[0])

    # Expand the grid horizontally to the right.
    for _ in range(4):
        for row in grid:
            # Get the row of the last tile.
            last_tile_row = row[-original_tile_width:]
            # Extend the current row with the values of the `last_tile_row + 1` and
            # wrap 9 to 1.
            row.extend((x + 1) if x < 9 else 1 for x in last_tile_row)
    # Expand the grid vertically downwards.
    for _ in range(4):
        # Loop through the rows of the above 5 tiles.
        for row in grid[-original_tile_height:]:
            # Add a new row that is +1 for each element in the previous tile's row and
            # wrap 9 to 1.
            new_row = [(x + 1) if x < 9 else 1 for x in row]
            grid.append(new_row)

    return grid


part2_grid = expand_grid(puzzle_input)
part2_min_risk = dijkstra(part2_grid)

print(f"Part 2 Solution: {part2_min_risk}")
