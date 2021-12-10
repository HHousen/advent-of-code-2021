from statistics import median

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

# Scores as defined by the challenge.
part1_character_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
part2_character_scores = {"]": 2, ")": 1, "}": 3, ">": 4}
open_to_close_character = {"(": ")", "[": "]", "{": "}", "<": ">"}

# These variables will hold the score of each line from the `puzzle_input`
part1_line_scores = []
part2_line_scores = []

for line in puzzle_input:
    # Initialize a `stack` to keep track of the open chunks.
    stack = []
    # Keep track of whether or not a line is corrupted (where a chunk closes with
    # the wrong character).
    corrupted = False
    for character in line:
        # If the current character is a character that opens a chunk, then add it to
        # the `stack`.
        if character in "([{<":
            stack.append(character)
        else:
            # Remove the starting character for the last-opened chunk from the `stack`
            # and store its matching closing character in `expected_character`.
            expected_character = open_to_close_character[stack.pop()]
            # If the current character is not the expected character, then the line is
            # corrupt and we can calculate the part 1 score for this line.
            if character != expected_character:
                # Get the score for this character, which is the first incorrect
                # closing character, and append it to `part1_line_scores`.
                part1_line_scores.append(part1_character_scores[character])
                corrupted = True
                break
    # After looping through each character, if the line is not marked as corrupted
    # (there are no incorrect characters, but it is missing some closing characters
    # at the end of the line) then calculate the part 2 score.
    if not corrupted:
        # We need to reverse the `stack` because the part 2 score is calculated in
        # the order of the characters used to close the line. Our `stack` contains
        # the most recent recent opening character at the end, so we must flip it.
        score = 0
        stack.reverse()
        # For each character, multiply the total score by 5 and then increase the
        # total score by the point value given for the character in
        # `part2_character_scores`.
        for character in stack:
            score = (
                score * 5 + part2_character_scores[open_to_close_character[character]]
            )
        part2_line_scores.append(score)

part1_solution = sum(part1_line_scores)
print(f"Part 1 Solution: {part1_solution}")

part2_solution = median(part2_line_scores)
print(f"Part 2 Solution: {part2_solution}")
