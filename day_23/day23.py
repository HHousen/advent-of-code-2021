from functools import cache  # Requires Python 3.9+

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.rstrip() for line in puzzle_input]

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

targets = {"A": 2, "B": 4, "C": 6, "D": 8}

final_rooms = {1: "A", 2: "B", 3: "C", 4: "D"}

doors = list(targets.values())


def get_top_idx(room_list):
    top_idx = 0
    try:
        while room_list[top_idx] is None:
            top_idx += 1
    except IndexError:
        # Room is empty so there is nothing to do
        return -1
    return top_idx


def possible_moves(state):
    # Break the possible moves into two move types: (1) moving from a room into the
    # hallway and (2) from the hallway into a room.
    # Move (1): Loop over the rooms and move the top amphipod in each room.
    for room_idx, _ in enumerate(state[1:]):
        room_idx += 1
        # Find the index of the top amphipod in the current room.
        top_idx = get_top_idx(state[room_idx])
        if top_idx == -1:
            # Room is empty so there is nothing to do
            continue
        # Convert `state` to lists so they are mutable.
        new_state = list(map(list, state))
        # The `amphipod_being_moved` is the amphipod at the top of the current room.
        amphipod_being_moved = state[room_idx][top_idx]
        # If all the amphipods in this room are in their correct final room, then don't
        # move the top amphipod and simply `continue` to the next room.
        if all(
            final_rooms[room_idx] == amphipod for amphipod in state[room_idx][top_idx:]
        ):
            continue
        hallway_position = doors[room_idx - 1]
        # Set the current amphipod position to None since it will be moved in the
        # following lines.
        new_state[room_idx][top_idx] = None
        # Create a list to hold the valid locations that amphipods can end up in the
        # `hallway`.
        possible_locations = []
        # The `hallway` is the first row of the `state`.
        hallway = new_state[0]
        # Loop over the possible hallway locations to the left of the current room.
        left_idxs = range(hallway_position)
        for left_idx in left_idxs:
            # The current location in the hallway is only possible to reach if it is
            # not directly outside a room because "amphipods will never stop on the
            # space immediately outside any room."
            if left_idx not in doors:
                possible_locations.append(left_idx)
            # If the hallway (`new_state[0]`) contains an amphipod at the current
            # position, then that space and all the spaces before it are invalid
            # and cannot be reached, so clear the list of `possible_locations`.
            # We do not break the loop here since positions to the right of the
            # occupied spot are still accessable.
            if hallway[left_idx] is not None:
                possible_locations.clear()

        hallway_length = len(hallway)
        # Loop over the possible hallway locations to the right of the current room.
        for right_idx in range(hallway_position, hallway_length):
            # Apply the tests in the opposite order as when searching to the left. If
            # a hallway position is occupied then break the loop because a amphipod
            # cannot move past another amphipod in the hallway.
            if hallway[right_idx] is not None:
                break
            # This is the same as when searching the hallway to the left. Amphipods
            # cannot stop directly outside of a room, so exclude those spaces.
            if right_idx not in doors:
                possible_locations.append(right_idx)
        # Convert the `new_state` back to tuples so they are hashable and can be cached
        # as part of memoization in `steps_to_final`.
        new_state = list(map(tuple, new_state))
        for location in possible_locations:
            # Convert the `hallway` to a list so it is mutable.
            hallway_list = list(hallway)
            # Move the amphipod to each `location` of the valid `possible_locations`.
            hallway_list[location] = amphipod_being_moved
            # Save the `hallway_list` back into the `new_state`.
            new_state[0] = tuple(hallway_list)
            # Yield the `new_state` and the amount of energy required to move the
            # amphipod to its possible location. `1+top_idx` is the number of moves
            # required to get into the hallway. `abs(location-hallway_position)` is the
            # number of moves to get from the door in the hallway to the final possible
            # position in the hallway. Finally, we multiply the number of moves by the
            # energy cost of per move of the amphipod type being moved.
            num_moves = 1 + top_idx + abs(location - hallway_position)
            energy = num_moves * costs[amphipod_being_moved]
            yield tuple(new_state), energy

    # Move (2): Loop over the positions in the hallway and move amphipods in the
    # hallway into rooms.
    for hallway_idx, hallway_position in enumerate(state[0]):
        if hallway_position is None:
            continue

        desired_room_idx = targets[hallway_position]
        # Get the `room_idx` of the target room for the amphipod at the current
        # `hallway_idx`.
        target_room_idx = desired_room_idx // 2
        room_set = set(state[target_room_idx])
        # Ignore any positions in the `room_set` that are not occupied.
        room_set.discard(None)

        # "Amphipods will never move from the hallway into a room unless that room is
        # their destination room and that room contains no amphipods which do not also
        # have that room as their own destination." So, if the room is occupied with
        # only one amphipod type and that amphipod type does not match the type of the
        # one at `hallway_idx`, then we cannot move the current amphipod into its
        # target room, so try the next amphipod in the hallway.
        if room_set and {hallway_position} != room_set:
            continue

        # If the position of current amphipod (`hallway_idx`) is to the *left* of its
        # `desired_room_idx`, then check if its path to the *right* is clear of other
        # amphipods.
        if hallway_idx < desired_room_idx:
            sl = slice(hallway_idx + 1, desired_room_idx + 1)
        # Otherwise, if the position of current amphipod is to the *right* of its
        # `desired_room_idx`, then check if its path to the *left* is clear of other
        # amphipods.
        else:
            sl = slice(desired_room_idx, hallway_idx)
        # Check if the current amphipod's path to its desired room is clear. Make sure
        # that all spots on the path are not occupied.
        if all(t is None for t in state[0][sl]):
            # Create a `new_state` that is the same as `state` but as lists so it is
            # mutable.
            new_state = list(map(list, state))
            # Remove the amphipod from the hallway.
            new_state[0][hallway_idx] = None

            room_list = new_state[target_room_idx]
            # Find the index of the bottom (last) `None` in the target room.
            for top_idx, val in reversed(list(enumerate(room_list))):
                if val is None:
                    break
            # Put the amphipod in the `top_index` of its target room.
            room_list[top_idx] = hallway_position
            # Yield the `new_state` and the amount of energy required to move the
            # amphipod to its new location. The math is the same as in case (1) when
            # moving from a room to the hallway.
            num_moves = 1 + top_idx + abs(hallway_idx - desired_room_idx)
            energy = num_moves * costs[hallway_position]
            yield tuple(map(tuple, new_state)), energy


# Use memoization so duplicate calculations are not performed and code executes
# quickly.
@cache
def steps_to_final(state, target_state):
    # If the current `state` is the `target_state`, then return a cost of 0 so it is
    # chosen.
    if state == target_state:
        return 0
    # Calculate all the possible moves from the current `state` and for each possible
    # move recursively calculate the cost plus the steps from that state to the final
    # `target_state`.
    possible_costs = [float("inf")] + [
        cost + steps_to_final(new_state, target_state)
        for new_state, cost in possible_moves(state)
    ]
    # Return the lowest cost out of the possible moves to reach the `target_state`.
    return min(possible_costs)


def initialize(puzzle_input):
    puzzle_input = [[line[idx] for idx in (3, 5, 7, 9)] for line in puzzle_input[2:-1]]
    # `state1` for my part 1 input is:
    # `((None, None, None, None, None, None, None, None, None, None, None), ('D', 'C'), ('B', 'A'), ('A', 'D'), ('C', 'B'))`
    starting_state = ((None,) * 11,) + tuple(zip(*puzzle_input))

    room_size = len(starting_state[1])
    # `target_state` for part 1 is always:
    # `((None, None, None, None, None, None, None, None, None, None, None), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))`
    target_state = ((None,) * 11,) + tuple((x,) * room_size for x in costs)
    return starting_state, target_state


starting_state, target_state = initialize(puzzle_input)
part1_solution = steps_to_final(starting_state, target_state)
print(f"Part 1 Solution: {part1_solution}")

puzzle_input.insert(3, "  #D#C#B#A#")
puzzle_input.insert(4, "  #D#B#A#C#")
starting_state, target_state = initialize(puzzle_input)
part2_solution = steps_to_final(starting_state, target_state)
print(f"Part 2 Solution: {part2_solution}")
