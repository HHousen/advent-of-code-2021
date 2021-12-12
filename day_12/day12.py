from collections import defaultdict

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip().split("-") for line in puzzle_input]

# Create a dictionary so we can look up a cave and get a list of the caves that are
# connected to it.
cave_connections = defaultdict(list)
for cave_a, cave_b in puzzle_input:
    cave_connections[cave_a].append(cave_b)
    cave_connections[cave_b].append(cave_a)


def find_paths(cave_name, small_caves_seen, duplicate_cave_visited, allow_duplicate):
    """Find the number of paths starting at the `cave_name` cave and ending at the
    "end" cave.

    Args:
        cave_name (str): The cave name to begin searching from.
        small_caves_seen (set): A set of small caves that have already been visited
            and cannot be visited again.
        duplicate_cave_visited (boolean): Wheather or not a single small cave has been
            visited twice (for part 2).
        allow_duplicate (boolean): If a single small cave is allowed to be visited
            twice. This distinguishes part 1 from part 2.

    Returns:
        int: The number of paths from "start" to "end".
    """
    # If we are at the end then return `1`` since we have found a valid path.
    if cave_name == "end":
        return 1
    # If we are finding paths in part 2 and the `cave_name` is "start" or "end" and
    # we have seen at least once small cave, then return 0 because the "start" and
    # "end" caves can only be visited once and cannot be the single duplicate cave.
    if allow_duplicate and cave_name in ["start", "end"] and small_caves_seen:
        return 0
    # Make a copy of the `small_caves_seen` to prevent the same `small_caves_seen`
    # from being shared among all calls to `find_paths`.
    new_small_caves_seen = small_caves_seen.copy()
    # If the cave is a small cave and it has already been visited, return 0 because
    # this is an invalid path... unless we are allowing a single duplicate small cave
    # and the duplicate cave has not yet been visited.
    if cave_name.islower():
        if cave_name in small_caves_seen:
            if allow_duplicate and not duplicate_cave_visited:
                duplicate_cave_visited = True
            else:
                return 0
        # Always add the small cave to the list of `small_caves_seen` so it is not
        # visited twice.
        new_small_caves_seen.add(cave_name)
    # Compute the number of paths from each cave connected to this cave and sum them
    # by recursively calling this (`find_paths`) function.
    num_paths = sum(
        find_paths(
            adjacent_cave,
            new_small_caves_seen,
            duplicate_cave_visited,
            allow_duplicate,
        )
        for adjacent_cave in cave_connections[cave_name]
    )
    # Finally, return the number of valid paths.
    return num_paths


# Find the number of paths when you can visit small caves at most once.
part1_num_paths = find_paths("start", set(), None, allow_duplicate=False)
print(f"Part 1 Solution: {part1_num_paths}")
# Find the number of paths when you can visit a single small cave twice.
part2_num_paths = find_paths("start", set(), False, allow_duplicate=True)
print(f"Part 2 Solution: {part2_num_paths}")
