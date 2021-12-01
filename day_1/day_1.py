with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [int(line.strip()) for line in puzzle_input]


def count_greater(data):
    return sum(item > data[idx] for idx, item in enumerate(data[1:]))
    # Alternative option using `zip`:
    # return sum(second > first for first, second in zip(data, data[1:]))


part1_solution = count_greater(puzzle_input)
print(f"Part 1 Solution: {part1_solution}")

sliding_window_data = [
    sum(puzzle_input[i - 1 : i + 2]) for i in range(1, len(puzzle_input))
]
# Alternative option using `zip`:
# sliding_window_data = [sum(w) for w in zip(puzzle_input, puzzle_input[1:], puzzle_input[2:])]
part2_solution = count_greater(sliding_window_data)

print(f"Part 2 Solution: {part2_solution}")
