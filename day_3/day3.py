from collections import Counter

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]


def get_most_common(s):
    return Counter(s).most_common(1)[0][0]


puzzle_input_transposed = zip(*puzzle_input)

most_common = "".join(get_most_common(column) for column in puzzle_input_transposed)

least_common = "".join([str(1 - int(x)) for x in most_common])

most_common_decimal = int(most_common, 2)
least_common_decimal = int(least_common, 2)

print(f"Part 1 Solution: {most_common_decimal*least_common_decimal}")


def search_bits(puzzle_input, default_new_num="1", common=0):
    oxygen_or_co2 = ""
    current = puzzle_input
    for col_idx in range(len(puzzle_input[0])):
        if len(current) == 1:  # if there is only one number left then it is the answer
            oxygen_or_co2 = current[0]
            break
        column = [num[col_idx] for num in current]
        c = Counter(column)
        if c["0"] == c["1"]:  # if 0 and 1 are equally common
            new_num = default_new_num
        else:
            new_num = c.most_common()[common][0]  # common=-1 gets least common
        oxygen_or_co2 += new_num
        # keep diagnostic numbers that contain the most/least common bit in the current position
        current = [x for x in current if x[col_idx] == new_num]
    return oxygen_or_co2


oxygen = search_bits(puzzle_input, default_new_num="1", common=0)
co2 = search_bits(puzzle_input, default_new_num="0", common=-1)

print(f"Part 2 Solution: {int(co2,2)*int(oxygen,2)}")
