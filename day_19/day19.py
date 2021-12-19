import math
from itertools import combinations
import numpy as np
from scipy.spatial.distance import cdist

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip().split("\n\n")

# Parse the `puzzle_input` into a list of lists which each inner list represents the
# beacons detected by scanner coresponding to the inner list's index in the outer list.
beacons_seen_by_scanners = [
    np.array(
        [
            list(map(int, coordinates.split(",")))
            # Remove the first line with `[1:]` since it simply contains the id of the
            # scanner like so: `--- scanner 0 ---`.
            for coordinates in scanner.split("\n")[1:]
        ]
    )
    for scanner in puzzle_input
]


def rotations():
    """Generate all possible rotation functions"""
    # This `rotations` function was taken from:
    # https://www.reddit.com/r/adventofcode/comments/rjpf7f/2021_day_19_solutions/hp5icay/
    vectors = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    vectors = list(map(np.array, vectors))
    for vi in vectors:
        for vj in vectors:
            if vi.dot(vj) == 0:
                vk = np.cross(vi, vj)
                yield lambda x: np.matmul(x, np.array([vi, vj, vk]))


def get_beacon_distances(scanner_map):
    """
    Calculate the distances between all the beacons that a single scanner detects.
    The distances between beacons will be the same even if the beacons are viewed from
    a different orientation or location (aka from a different scanner).
    """
    num_beacons = len(scanner_map)
    # For each combination of 2 beacons indexes, create a dictionary of the distance
    # between them and their indexes in the `scanner_map`. The dictionary will have the
    # form: `(a, b, c): (idx_a, idx_b)`, where `a`, `b`, and `c` are sorted from
    # smallest to largest.
    return {
        tuple(sorted(abs(scanner_map[idx_a] - scanner_map[idx_b]))): (idx_a, idx_b)
        for idx_a, idx_b in combinations(range(num_beacons), 2)
    }


def find_overlapping_maps(beacon_distances):
    # If two scanner maps overlap, then they will have C(12,2) (12 choose 2) common
    # elements. C(12,2) equals 66. So, the number of ways to choose 2 items from 12 items
    # (without repetition and without order) is 66. `get_beacon_distances` gets the
    # distances between every combination of 2 beacons, so we account for that in this
    # function by checking that at least C(12,2) distances are the same.
    overlap_threshold = math.comb(12, 2)  # `math.comb(12, 2)` = 66.
    # These two nested for loops technically calculate all the permutations (order
    # matters, so we would get (a,b) and (b,a)) but all we need is to calculate
    # combinations (order doesn't matter, so we would get (a,b) but not (b,a)).
    # However, this doesn't make much of a difference and this format is easier to
    # read.
    for idx_a, beacon_distances_a in enumerate(beacon_distances):
        for idx_b, beacon_distances_b in enumerate(beacon_distances):
            # Find the common distances between the beacons of the two `scanner_map`s
            # being tested.
            overlapping_beacon_distances = set(beacon_distances_a.keys()) & set(
                beacon_distances_b.keys()
            )
            # If the number of `overlapping_beacon_distances` is greater than C(12,2),
            # then we have match and we can figure out the scanner's position relative
            # to the first scanner.
            if len(overlapping_beacon_distances) >= overlap_threshold:
                # Yield the scanner ids of the overlapping scanners as well as the
                # first `overlapping_beacon_distances` so we can look up the
                # corresponding beacon ids and correctly rotate them later.
                first_overlapping_beacon_distance = overlapping_beacon_distances.pop()
                yield idx_a, idx_b, first_overlapping_beacon_distance


def fit(
    scanner_map_a,
    scanner_map_b,
    scanner_a_beacon_pair,
    scanner_b_beacon_pair,
):
    """
    Find the correct rotation/translation to make `scanner_map_a` fit to
    `scanner_map_b`.
    """
    # For each of the 24 possible rotations...
    for rotate in rotations():
        # Rotate `scanner_map_b` (the scanner map to be oriented correctly)
        scanner_map_b_rotated = rotate(scanner_map_b)
        # Loop through the two possible beacons for scanner B that could match with
        # the first beacon in the beacon pair for scanner A (`scanner_a_beacon_pair[0]`).
        # We want to find the beacons that match between the two scanner maps. We have
        # 4 beacons: 2 for each scanner's `beacon_pair`. One of the beacon ids from the
        # scanner A's pair will match with one of the beacon ids from scanner B's pair.
        # So, we assume that scanner A's fist beacon in the pair is the one that
        # matches and then we test it against both of scanner B's beacons in its pair.
        for scanner_b_current_beacon in scanner_b_beacon_pair:
            # Calculate the translation required to shift `scanner_map_b_rotated` to
            # `scanner_map_a` so that the beacons overlap.
            translation = (
                scanner_map_a[scanner_a_beacon_pair[0]]
                - scanner_map_b_rotated[scanner_b_current_beacon]
            )

            # Apply the translation to the rotated `scanner_map_b` and convert it from
            # a numpy array to a set of tuples so that the intersection can be easily
            # computed.
            scanner_map_b_rotated_translated = set(
                map(tuple, scanner_map_b_rotated + translation)
            )
            scanner_map_a_set = set(map(tuple, scanner_map_a))
            # If the number of overlappign beacons is greater than or equal to 12 then
            # the rotation and translation are correct so return them.
            if len(scanner_map_b_rotated_translated & scanner_map_a_set) >= 12:
                return translation, scanner_map_b_rotated_translated, rotate


def solve(beacons_seen_by_scanners):
    num_scanners = len(beacons_seen_by_scanners)
    scanner_positions = {0: np.array([0, 0, 0])}
    beacons = set(tuple(x) for x in beacons_seen_by_scanners[0])
    beacon_distances = [
        get_beacon_distances(scanner_map) for scanner_map in beacons_seen_by_scanners
    ]
    while len(scanner_positions) < num_scanners:
        for (
            scanner_idx_a,
            scanner_idx_b,
            first_overlapping_beacon_distance,
        ) in find_overlapping_maps(beacon_distances):
            # If `scanner_idx_a` is in the `scanner_positions` dictionary or if
            # `scanner_idx_b` is in the `scanner_positions` dictionary but not both,
            # then skip this iteration. We must start with a scanner that is in the
            # dictionary so we can find a way to fit the new scanner to the positions
            # of the beacons for the scanner that is already in the dictionary. If both
            # scanners are in the dictionary then they are both already aligned and
            # there is no point doing the calculations again.
            if not (scanner_idx_a in scanner_positions.keys()) ^ (
                scanner_idx_b in scanner_positions.keys()
            ):
                continue
            if scanner_idx_b in scanner_positions.keys():
                # Always ensure that `scanner_idx_b` is the scanner being added.
                scanner_idx_a, scanner_idx_b = scanner_idx_b, scanner_idx_a

            # `beacon_distances[scanner_idx_a]` is the dictionary of distances and
            # beacon indexes created by `get_beacon_distances`. We are selecting the
            # value at `first_overlapping_beacon_distance`, which is the pair of
            # beacons with distance `first_overlapping_beacon_distance`. In other
            # words, `first_overlapping_beacon_distance` is the distance between the
            # pair of beacons `scanner_a_beacon_pair` for the scanner with id
            # `scanner_idx_a`.
            scanner_a_beacon_pair = beacon_distances[scanner_idx_a][
                first_overlapping_beacon_distance
            ]
            # `scanner_b_beacon_pair` is the pair of beacons with distance
            # `first_overlapping_beacon_distance` as seen by the scanner with id
            # `scanner_idx_b`.
            scanner_b_beacon_pair = beacon_distances[scanner_idx_b][
                first_overlapping_beacon_distance
            ]

            # Get the scanner maps (aka the list of beacons as seen by the
            # corresponding `scanner_idx`) for the scanner we are trying to fit to (a)
            # and the scanner we are trying to fit (b).
            scanner_map_a = beacons_seen_by_scanners[scanner_idx_a]
            scanner_map_b = beacons_seen_by_scanners[scanner_idx_b]

            # `fit` `scanner_map_b` to `scanner_map_a` using the
            # `scanner_a_beacon_pair` and `scanner_b_beacon_pair`.
            scanner_positions[scanner_idx_b], new_beacons, rot = fit(
                scanner_map_a,
                scanner_map_b,
                scanner_a_beacon_pair,
                scanner_b_beacon_pair,
            )
            # Use the rotate function return from `fit` to rotate the beacons seen by
            # scanner B into the correct position. Add the position of scanner B
            # relative to the first scanner, which is located at (0, 0, 0), to each of
            # the beacon positions since the beacons were originally give as relative
            # to scanner B.
            beacons_seen_by_scanners[scanner_idx_b] = (
                rot(beacons_seen_by_scanners[scanner_idx_b])
                + scanner_positions[scanner_idx_b]
            )
            # Add the `new_beacons` to the current set of `beacon` coordinates.
            beacons = beacons.union(new_beacons)

    return scanner_positions.values(), beacons


scanner_positions, beacons = solve(beacons_seen_by_scanners)
# Calculate the total number of beacons for part 1.
part1_solution = len(beacons)
print(f"Part 1 Solution: {part1_solution}")

largest_manhattan_distance = max(  # Find the largest distance out of all distances.
    int(
        cdist(  # `cdist` computes distance between two points.
            np.reshape(
                scanner_a_position, (-1, 3)
            ),  # Reshape from 1D to 2D since `cdist` needs 2D.
            np.reshape(scanner_b_position, (-1, 3)),
            metric="cityblock",  # Use the Manhattan distance.
        )[0][
            0
        ]  # Extract the actual value embedded within two nested lists.
    )
    # Loop through all the possible combinations of two scanner positions
    for scanner_a_position, scanner_b_position in combinations(scanner_positions, 2)
)
print(f"Part 2 Solution: {largest_manhattan_distance}")
