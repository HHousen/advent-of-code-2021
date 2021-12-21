from functools import cache
from itertools import product
from collections import Counter

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip() for line in puzzle_input]

position1, position2 = [int(x.split()[-1]) for x in puzzle_input]


def run_part1_turn(position, num_die_rolls):
    # If the player's `position` is a multiple of 10, then the `mod 10` will set it to
    # 0. So, we use the `or 10` expression so that if the new position is 0, it gets
    # set to 10 instead. The expression `3 * num_die_rolls + 6` is determined from the
    # fact that the die increases by one each roll. This is the same as rolling the die
    # 3 times and getting the same number and then adding 6. Each roll of the real die
    # adds 1 to the previous roll so from the perspective of the first roll, the nth
    # next roll will be the first roll value + n.
    position = (position + 3 * num_die_rolls + 6) % 10 or 10
    # Each turn the player rolls the die 3 times.
    num_die_rolls += 3
    return position, num_die_rolls


def part1(position1, position2):
    num_die_rolls = 0
    # Each player has a list with two elements: their current position and score.
    players = [[position1, 0], [position2, 0]]
    # Keep looping until a player reaches a score of 1000 or greater.
    while True:
        # Each player performs the same actions.
        for player in players:
            # Update the current player's position and the number of times the die was
            # rolled.
            player[0], num_die_rolls = run_part1_turn(player[0], num_die_rolls)
            # Add the player's current position to their current score.
            player[1] += player[0]
            # If the player has reached a score of 1000 or above, then the game is
            # complete. Return the values requested by the challenge description.
            if player[1] >= 1000:
                return min(players[0][1], players[1][1]) * num_die_rolls


part1_solution = part1(position1, position2)
print(f"Part 1 Solution: {part1_solution}")

# The next line creates the following list:
# `[(6, 7), (5, 6), (7, 6), (4, 3), (8, 3), (3, 1), (9, 1)]`.
# This represents the possible outcomes for the dice rolls. For instance, you can roll
# a 6 in 7 ways, a 5 in 6 ways, a 7 in 6 ways, etc. The 3 sided die is rolled 3 times
# each turn.
sum_possibilities = Counter(
    sum(r) for r in product(range(1, 4), repeat=3)
).most_common()

# `@cache` is a feature of Python 3.9+ that implemented dictionary based memoization.
@cache
def part2(position1, position2, score1=0, score2=0):
    # If the score of the previously updated player is 21 or greater, then the game is
    # over. Return 0 for the losing player and for the winning player so each player
    # gets the correct number of wins.
    if score2 >= 21:
        return 0, 1

    wins1, wins2 = 0, 0
    for roll, num_ways in sum_possibilities:
        # Use the same logic from part 1 to set a score of a multiple of 10 to 10
        # instead of 0.
        position1_updated = (position1 + roll) % 10 or 10
        # Swap the player's positions and scores with each call to `part2`. This means
        # the each call to the function only has to update one player since then next
        # call will update the other player.
        new_wins2, new_wins1 = part2(
            position2, position1_updated, score2, score1 + position1_updated
        )
        # Compute the number of wins by adding to the previous number of wins the
        # number of wins earned by each roll times the number of ways that roll could
        # occur.
        wins1, wins2 = wins1 + num_ways * new_wins1, wins2 + num_ways * new_wins2

    # Return the total number of wins for each player.
    return wins1, wins2


part2_solution = max(part2(position1, position2))
print(f"Part 2 Solution: {part2_solution}")
