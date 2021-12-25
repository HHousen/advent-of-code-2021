with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [list(line.strip()) for line in puzzle_input]

height = len(puzzle_input)
width = len(puzzle_input[0])


def run_east(grid):
    moves = []
    # Loop over each element in the grid.
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            # If the value in the grid is east and the destination cell is empty, then
            # append these grid coordinates as a sea cucumber that can move.
            # `(col_idx + 1) % width` will wrap around to the other side of the grid
            # in the same row if the current sea cucumber is on the edge of the grid.
            if value == ">" and row[(col_idx + 1) % width] == ".":
                moves.append((row_idx, col_idx))

    # For each set of coordinates in `moves`, set the position to "empty," and set the
    # sea cucumber's destination to its representation symbol.
    for row_idx, col_idx in moves:
        grid[row_idx][col_idx] = "."
        grid[row_idx][(col_idx + 1) % width] = ">"

    # Return the new `grid` and the number of moves completed.
    return grid, len(moves)


def run_south(grid):
    # Does the exact same actions as `run_east()` but for the southern moving sea
    # cucumbers. These sea cucumbers wrap from the bottom to the top of the grid
    # and use the symbol `v` instead of `>`.
    moves = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == "v" and grid[(row_idx + 1) % height][col_idx] == ".":
                moves.append((row_idx, col_idx))

    for row_idx, col_idx in moves:
        grid[row_idx][col_idx] = "."
        grid[(row_idx + 1) % height][col_idx] = "v"

    return grid, len(moves)


step = 0
current_step_num_moves = -1
# Keep looping until the number of moves performed in a single step is zero, which
# indicates that none of the sea cucumbers moved in that step.
while current_step_num_moves != 0:
    # First, move the eastward facing sea cucumbers.
    puzzle_input, num_moves = run_east(puzzle_input)
    current_step_num_moves = num_moves
    # Then, move the southward facing sea cucumbers.
    puzzle_input, num_moves = run_south(puzzle_input)
    current_step_num_moves += num_moves

    step += 1


print(f"Part 1 Solution: {step}")
