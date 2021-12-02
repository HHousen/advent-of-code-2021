with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip().split() for line in puzzle_input]

horizontal = 0
depth = 0
for command, amount in puzzle_input:
    if command == "forward":
        horizontal += int(amount)
    elif command == "up":
        depth -= int(amount)
    elif command == "down":
        depth += int(amount)

print(f"Part 1 Solution: {horizontal*depth}")

aim = 0
horizontal = 0
depth = 0
for command, amount in puzzle_input:
    if command == "forward":
        horizontal += int(amount)
        depth += int(amount) * aim
    elif command == "up":
        aim -= int(amount)
    elif command == "down":
        aim += int(amount)

print(f"Part 2 Solution: {horizontal*depth}")
