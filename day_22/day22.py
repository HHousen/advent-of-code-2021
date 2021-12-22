import re
from collections import defaultdict

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = [line.strip().split() for line in puzzle_input]


def intersect(nx0, nx1, ny0, ny1, nz0, nz1, ox0, ox1, oy0, oy1, oz0, oz1):
    # The first six parameters of this function are one set of coordinates and the last
    # six are another set of coordinates. In this case, the `n` represents the new
    # coordinates and the `o` represents the old coordinates from the `solve` function.
    # This function finds and returns the intersection between two cuboids.
    ix0 = max(nx0, ox0)
    ix1 = min(nx1, ox1)
    iy0 = max(ny0, oy0)
    iy1 = min(ny1, oy1)
    iz0 = max(nz0, oz0)
    iz1 = min(nz1, oz1)
    if ix0 <= ix1 and iy0 <= iy1 and iz0 <= iz1:
        return ix0, ix1, iy0, iy1, iz0, iz1
    return None


def solve(part1=False):
    cubes = defaultdict(int)
    for on_off, coordinates in puzzle_input:
        # Convert `on_off` from a `str` to a `bool` indicating if this cuboid is "on".
        on_off = on_off == "on"
        # `-?\d+` matches 0 or 1 "-" characters and then matches 1 or more digit
        # characters (0-9). Convert all matches to an integer using `map(int, ...)`.
        new_coords = tuple(map(int, re.findall("-?\d+", coordinates)))
        # If we are solving part 1, then break the loop and return immediately if any
        # of the new coordinates are outside a 50x50x50 region centered at (0,0).
        if part1 and any([abs(x) > 50 for x in new_coords]):
            break

        # Check if the current cuboid (`new_coords`) intersects with any "on" or
        # intersection cuboid that we have encountered. If there is an intersection,
        # then add a new cube for the intersection with the opposite sign. This will
        # cancel out the "on"/"off" status of any cubes in the intersecting region.
        # These are the following cases that can happen:
        # - (A) A new "on" cuboid intersects an old "on" cuboid: The intersecting region
        #   gets added to the `cubes` dictionary with a value of `-1`. Thus, the sum of
        #   the states for the cubes in the intersecting region is `0` or "off.
        #   However, since the cube is "on", it gets added to the `cubes` dictionary,
        #   thus overriding the state of the intersecting region.
        # - (B) A new "on" cuboid intersects an old "off" cuboid: The intersecting region
        #   gets added to the `cubes` dictionary and its sign remains *off* (0). The
        #   new cube gets added to the `cubes` dictionary since it is "on". Thus, the
        #   intersecting region now has a value of "on" (1).
        # - (C) A new "off" cuboid intersects an old "on" cuboid: The intersecting region
        #   gets added to the `cubes` dictionary with a value of `-1`. Thus, the cubes
        #   in the intersecting region are *off* (0).
        # - (D) A new "off" cuboid intersects an old "off" cuboid: The intersecting region
        #   gets added to the `cubes` dictionary with a value of `0` (off).
        # TL;DR: For every intersection between the current cuboid and previously
        # encountered cuboids, subtract or add the value to make the region "off". Then
        # if the new cuboid is "on", store that new cuboid with the "on" value (1),
        # thus negating turning the intersecting region off.
        for old_coords, old_sign in cubes.copy().items():
            intersection = intersect(*new_coords, *old_coords)
            if intersection:
                cubes[intersection] -= old_sign

        if on_off:
            cubes[new_coords] += 1

        # The next line causes about a 1/3 speedup to execution time. It removes any
        # cuboids that have been turned "off" (their value has been set to `0`). This
        # causes cases B and D above to never occur, thus saving compute time.
        cubes = defaultdict(
            int, {key: value for key, value in cubes.items() if value != 0}
        )

    # Finally, return the number of cubes that are "on". This is the sum of the values
    # for each cube. This can be done by computing the volume of each region,
    # multiplying that volume by the on or off `state` of the region, and finallying
    # adding all those cuboid values together.
    return sum(
        (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * state
        for (x0, x1, y0, y1, z0, z1), state in cubes.items()
    )


part1_solution = solve(part1=True)
print(f"Part 1 Solution: {part1_solution}")
part2_solution = solve(part1=False)
print(f"Part 2 Solution: {part2_solution}")
