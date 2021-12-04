with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

# Parse input into lists
puzzle_input = puzzle_input.split("\n\n")
draw_order = puzzle_input[0].split(",")
boards = [[y.split() for y in x.split("\n")] for x in puzzle_input[1:]]


def get_board_score(final_board, numbers_drawn):
    # Flatten final board
    final_board_flat = [item for sublist in final_board for item in sublist]
    # Sum the board values that were not called
    sum_unmarked = sum(int(x) for x in final_board_flat if x not in numbers_drawn)
    return sum_unmarked * int(numbers_drawn[-1])


def get_winning_board(draw_order, boards):
    numbers_drawn = []
    for number_drawn in draw_order:
        numbers_drawn.append(number_drawn)
        for board in boards:
            # zip(*board) is transposed board matrix
            for row, column in zip(board, zip(*board)):
                # If all the values in a single row or column are in the list of
                # numbers drawn, then the board is a winner.
                if all([x in numbers_drawn for x in row]) or all(
                    [x in numbers_drawn for x in column]
                ):
                    return board, numbers_drawn


winning_board, numbers_drawn = get_winning_board(draw_order, boards)
part1_solution = get_board_score(winning_board, numbers_drawn)
print(f"Part 1 Solution: {part1_solution}")


def get_last_winning_board(draw_order, boards):
    numbers_drawn = []
    for number_drawn in draw_order:
        numbers_drawn.append(number_drawn)
        boards_to_remove = []
        for board in boards:
            # zip(*board) is transposed board matrix
            for row, column in zip(board, zip(*board)):
                # If all the values in a single row or column are in the list of
                # numbers drawn, then the board is a winner and it should be removed.
                if all([x in numbers_drawn for x in row]) or all(
                    [x in numbers_drawn for x in column]
                ):
                    boards_to_remove.append(board)
                    if len(boards) == 1:  # only one board left, must be losing board
                        return boards[0], numbers_drawn
                    break  # no need to continue checking board if it already won
        # Remove winning boards
        boards = [x for x in boards if x not in boards_to_remove]


last_winning_board, numbers_drawn = get_last_winning_board(draw_order, boards)
part2_solution = get_board_score(last_winning_board, numbers_drawn)
print(f"Part 2 Solution: {part2_solution}")
