from itertools import permutations
from tqdm import tqdm

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

puzzle_input = [x.split(" | ") for x in puzzle_input]


def solve_part1(puzzle_input):
    part1_input = [x[1] for x in puzzle_input]
    counter = 0
    for output_sequence in part1_input:
        for encoded_digit in output_sequence.split(" "):
            # 2, 4, 3, and 7 are the number of values needed to display a 1, 4, 7, and
            # 8, respectively. In other words, every output that is `len(2)` represents
            # a 1, every output that is `len(4)` represents a 4, etc.
            if len(encoded_digit) in [2, 4, 3, 7]:
                counter += 1
    return counter


part1_solution = solve_part1(puzzle_input)
print(f"Part 1 Solution: {part1_solution}")


# `desired_state` is taken directly from the challenge text. However, other
# combinations are also valid.
desired_state = {
    "acedgfb": 8,
    "cdfbe": 5,
    "gcdfa": 2,
    "fbcad": 3,
    "dab": 7,
    "cefabd": 9,
    "cdfgeb": 6,
    "eafb": 4,
    "cagedb": 0,
    "ab": 1,
}
# Sort the `desired_state` keys since the encoded digits in the input do no
# always have the letters in the same order.
desired_state = {"".join(sorted(k)): v for k, v in desired_state.items()}
# The labels that are used in `desired_state` and in `puzzle_input`
segment_labels = "abcdefg"


def decode_routing(display, routing_mapping):
    display_decoded = [
        "".join(routing_mapping[character] for character in encoded_digit)
        for encoded_digit in display
    ]
    # Sort because the encoded digits in the input do no always have the letters
    # in the same order.
    display_decoded = [
        "".join(sorted(decoded_digit)) for decoded_digit in display_decoded
    ]
    return display_decoded


# Note that this is a bruteforce solution, more efficeint solutions exist.
# For example, https://github.com/jonathanpaulson/AdventOfCode/blob/master/2021/8.py
# solves part 2 using a bruteforce and a smart approach.
display_values = []
for input_output_tuple in tqdm(puzzle_input, "Bruteforcing"):
    # `display_input` is a list of each encoded digit *before* the "|"
    display_input = input_output_tuple[0].split(" ")
    # `display_output` is a list of each encoded digit *after* the "|"
    display_output = input_output_tuple[1].split(" ")
    # For each possible permutation of the segment labels
    for segment_label_permutation in permutations(segment_labels):
        # `routing_mapping` maps the current guess for wire ids to the display segment ids.
        # In other words, the dictionary is of the form `wire_id: display_id`
        routing_mapping = dict(zip(segment_label_permutation, segment_labels))
        # Using the current guess for the `routing_mapping`, "decode" the `display_input`
        # by looping through each character in each digit and setting it to its new value
        # as per the `routing_mapping`.
        display_input_decoded = decode_routing(display_input, routing_mapping)
        # If all of the decoded digits in the `display_input` are in the `desired_state`,
        # then the bruteforce has found the valid `routing_mapping`. In other words, if
        # our bruteforced wire-id-to-display-segment-id mapping is correct, then all of
        # the decoded digits in the `display_input` will map to an integer as defined
        # by the `desired_state`.
        if all(
            decoded_digit in desired_state for decoded_digit in display_input_decoded
        ):
            # Decode the `display_output` using the valid `routing_mapping` in the same
            # way that the `display_input` was decoded.
            display_output_decoded = decode_routing(display_output, routing_mapping)
            # Finally, convert the decoded `display_output` to an integer by simply
            # mapping each digit to an integer using the `desired_state` dictionary.
            output_int = int(
                "".join(str(desired_state[x]) for x in display_output_decoded)
            )
            # Save our final decoded value.
            display_values.append(output_int)
            # Exit the bruteforce for the current line of `puzzle_input` to reduce
            # unnecessary computations.
            break


print(f"Part 2 Solution: {sum(display_values)}")
