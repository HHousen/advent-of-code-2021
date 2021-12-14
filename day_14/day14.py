from collections import Counter

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

polymer_template, pair_insertion_rules = puzzle_input.split("\n\n")

polymer_template = polymer_template.strip()
# Parse the `pair_insertion_rules` into a dictionary of the follwing form:
# `(pair_a, pair_b): insertion_char`.
pair_insertion_rules = dict(x.split(" -> ") for x in pair_insertion_rules.split("\n"))
pair_insertion_rules = {tuple(x): y for x, y in pair_insertion_rules.items()}

# Convert the starting `polymer_template` into a dictionary of the character counts.
character_counts = Counter(polymer_template)
# Count the pairs in the starting `polymer_template`. A pair consists of two adjacent
# characters. Pairs can overlap. We only loop to `len(polymer_template)-1` so that we
# do not go out of bounds on the list when we call `polymer_template[x+1]`.
pairs = Counter(
    (polymer_template[x], polymer_template[x + 1])
    for x in range(len(polymer_template) - 1)
)


def solve(num_steps, character_counts, pairs):
    # For each step...
    for _ in range(num_steps):
        # Make a copy of the `pairs` so that we can perform the pair insertions
        # simultaneously without worrying about modifying the dictionary we are
        # looping over.
        original_pairs = pairs.copy()
        # Loop over the state of the pairs from the previous iteration. For each
        # pair...
        for (pair_a, pair_b), pair_count in original_pairs.items():
            # Look up the character that should be inserted between this pair.
            new_char_to_insert = pair_insertion_rules[(pair_a, pair_b)]
            # Remove the count of the original pair, `(pair_a, pair_b)`, because it
            # will no longer exist once the `new_char_to_insert` is inserted.
            pairs[(pair_a, pair_b)] -= pair_count
            # Increase the count of the two replacement pairs. There are two new pairs
            # because pairs can overlap.
            pairs[(pair_a, new_char_to_insert)] += pair_count
            pairs[(new_char_to_insert, pair_b)] += pair_count
            # Finally, increase the count of the new character that was inserted. This
            # is not multipled by two again because pairs can overlap. Conceptually,
            # the same instance of this character is used in both pairs.
            character_counts[new_char_to_insert] += pair_count

    # Return the quantity of the most common element minus the quantity of the least
    # common element.
    return max(character_counts.values()) - min(character_counts.values())


# Use `.copy()` to ensure that each run to the function gets the original
# `puzzle_input` data.
part1_solution = solve(10, character_counts.copy(), pairs.copy())
print(f"Part 1 Solution: {part1_solution}")
part2_solution = solve(40, character_counts.copy(), pairs.copy())
print(f"Part 2 Solution: {part2_solution}")
