from collections import Counter, defaultdict

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

initial_state = [int(x) for x in puzzle_input.split(",")]

# My slow initial approach used for part 1:
# current_state = initial_state
# for day in range(80):
#     new_state = [x-1 for x in current_state]
#     num_new = new_state.count(-1)
#     new_state = [6 if x == -1 else x for x in new_state] + [8 for _ in range(num_new)]
#     current_state = new_state
# print(f"Part 1 Solution: {len(current_state)}")

# Count the number of fish at each age
age_to_count = Counter(initial_state)

def simulate_days(num_days, age_to_count):
    for _ in range(num_days):
        new_fish = defaultdict(int)
        # For each age and count tuple
        for age, count in age_to_count.items():
            # If the age is greater than zero, then decrement the `age` by setting the
            # `age - 1` key of `new_fish` to the count of fish for the current `age`.
            if age > 0:
                new_fish[age - 1] += count
            # If the age is zero, then spawn new fish and reset the spawn timers on
            # the current `age == 0` fish, as per the challenge requirements.
            else:
                new_fish[6] += count
                new_fish[8] += count
        # Store the `new_fish` for the next iteration/day
        age_to_count = new_fish
    
    # The number of fish is the sum of the number of fish at each age
    return sum(age_to_count.values())

print(f"Part 1 Solution: {simulate_days(80, age_to_count)}")
print(f"Part 2 Solution: {simulate_days(256, age_to_count)}")
