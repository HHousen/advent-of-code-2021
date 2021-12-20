import numpy as np
from scipy.ndimage import convolve

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip().split("\n\n")

# Number of steps to run the image enhancement algorithm for.
num_steps = 50

image_enhancement_algorithm, input_image = puzzle_input
# Parse the `image_enhancement_algorithm` by converting "#" to 1 and "." to 0.
image_enhancement_algorithm = np.array(
    [int(x == "#") for x in image_enhancement_algorithm]
)
# Parse the `input_image` into a numpy matrix, convert "#" to 1 and "." to 0, and pad
# the matrix so it has room to expand when "enhanced"/convolved.
input_image = np.pad(
    [[int(y == "#") for y in x] for x in input_image.split("\n")],
    (num_steps, num_steps),
)

# `np.arange(9)` creates an array of evenly spaced values from 0 (inclusive) to 9
# (exclusive): `array([0, 1, 2, 3, 4, 5, 6, 7, 8])`.
# Then, we raise 2 to the power of each element in this list to create an array capable
# of converting binary numbers to decimal: `[1, 2, 4, 8, 16, 32, 64, 128, 256]`.
# Finally, we reshape this from a (9,) vector into a (3, 3) matrix, which produces the
# following:
# [[  1   2   4]
#  [  8  16  32]
#  [ 64 128 256]]
kernel = 2 ** np.arange(9).reshape((3, 3))

image = input_image
for step in range(num_steps):
    # Perform the convolution:
    # https://en.wikipedia.org/wiki/Kernel_(image_processing)#Convolution
    image_convolved = convolve(image, kernel)
    # Look up each convolved value in the `image_enhancement_algorithm` and see if its
    # decimal equivalent should be a "." (0) or a "#" (1). Since the first index of the
    # `image_enhancement_algorithm` is 1 for my `puzzle_input` (not on the example
    # input), all the pixels will become lit (have a value of 1) on every odd numbered
    # step (an odd number of applications of the enhancement algorithm). However, this
    # is not an issue because the challenge never asks for the number of lit pixels at
    # an odd numbered step. Nevertheless, this problem can be solved by setting the
    # `convolve` function's `cval` parameter to `step % 2`.
    image = image_enhancement_algorithm[image_convolved]
    # The above line produces the same output as the below commented line:
    # image = np.array([[image_enhancement_algorithm[y] for y in x] for x in image_convolved])
    if step == 1:
        # If we have completed 2 steps, then count the number of lit pixels and return
        # the answer to the first part.
        part1_solution = image.sum()
        print(f"Part 1 Solution: {part1_solution}")

# Count the number of pixels after `num_steps` (50) steps.
part2_solution = image.sum()
print(f"Part 2 Solution: {part2_solution}")
