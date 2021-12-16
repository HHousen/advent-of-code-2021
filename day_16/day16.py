from operator import add, mul, gt, lt, eq
from functools import reduce

with open("puzzle_input.txt", "r") as puzzle_input:
    puzzle_input = puzzle_input.read().strip()

# A list to keep track of the versions of all packets.
packet_versions = []

# Convert the puzzle input from hexadecimal to binary.
binary_packets = bin(int(puzzle_input, 16))[2:]
# Pad the input according to the challenge instructions.
while len(binary_packets) < 4 * len(puzzle_input):
    binary_packets = "0" + binary_packets
# Reverse the binary packets so we can easily pop off bit by bit.
binary_packets = list(binary_packets)
binary_packets.reverse()
# Convert each binary digit from a string to an integer.
binary_packets = [int(x) for x in binary_packets]


def read_bits(data, num_bits):
    """
    Return a generator that pops off `num_bits` from `data`.
    """
    # Using `list.pop()` is valid since we reversed the binary data.
    for _ in range(num_bits):
        yield data.pop()


def to_decimal(binary_list):
    """
    Convert a list of binary digits to a decimal integer.
    """
    res = 0
    for ele in binary_list:
        res = (res << 1) | ele
    return res


def read_num(data, num_bits):
    """
    Same as `read_bits`, but converts the popped data to decimal using `to_decimal`
    """
    return to_decimal(read_bits(data, num_bits))


# Define the operations for the operator packets. The position of the operation
# corresponds to the packet's `type_id`.
operations = [add, mul, min, max, lambda x, y: (x << 4) | y, gt, lt, eq]


def parse(data):
    # Keep track of `packet_versions` accross all function calls.
    global packet_versions

    # Read the `version` and `type_id` from the first packet.
    version = read_num(data, 3)
    type_id = read_num(data, 3)

    # Add the version of the packet to the `packet_versions` list.
    packet_versions.append(version)

    def get_subpackets():
        # If the `type_id` is 4 then the packet is a literal value. Pop off the
        # first bit of each chunk and then yield the 4-bit chunk until the first bit
        # of the 5-bit chunks is 0 (represents the last chunk).
        if type_id == 4:
            while True:
                # In this loop we need to yield the chunk even if it is the last chunk
                # so we use `while True` and a return statement.
                done = not data.pop()
                yield read_num(data, 4)
                if done:
                    return
        # If the packet is an operator packet...
        else:
            length_type_id = read_num(data, 1)
            if length_type_id:  # If the `length_type_id` is 1.
                # `read_num(data, 11)` represents the number of subpackets in this
                # operator packet. Loop through them and yield them.
                for _ in range(read_num(data, 11)):
                    yield parse(data)
            else:  # If the `length_type_id` is 0.
                # `bit_length` is the number of bits of packets in the operator packet.
                bit_length = read_num(data, 15)
                bits_remaining_when_operator_done = len(data) - bit_length
                # We will keep looping through and parsing the packet `data` until the
                # length of the data equals the number of bits that should remain once
                # the operator packet is complete.
                while len(data) != bits_remaining_when_operator_done:
                    yield parse(data)

    # Get the operation for the current packet.
    operation = operations[type_id]
    # Run this operation on all the subpackets of this packet.
    return reduce(operation, get_subpackets())


final_packet_output = parse(binary_packets)
packet_versions_sum = sum(packet_versions)

print(f"Part 1 Solution: {packet_versions_sum}")
print(f"Part 2 Solution: {final_packet_output}")
