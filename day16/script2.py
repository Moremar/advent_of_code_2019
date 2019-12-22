from day16.script1 import get_digits
import itertools

# With an input 10000 times longer, the brute-force we did in part 1 does not work
# This time we want an offset of the first 7 digits, which is more than half of the input
# We notice that :
#  - to calculate the digit at index i, we need only the input digits from index i and above
#    therefore all digits before the offset does not need to be calculated at any phase
#  - for an index i bigger than half of the input size, the coefs of the pattern are 0 until i and 1 after
#    this means all coefs can be calculated from a partial sum of the input
#
# This time the steps will be :
# - from the very long input, keep only the digits after the offset as our input
# - at each step, calculate the next phase as the first digit of the partial sum of the input


def get_next_phase(phase):
    # 1st digit is the unit digit of the sum of all digits of the previous phase
    # 2nd digit is the unit digit of the sum of all digits except the first
    # ...
    # last digit is the last digit of the previous phase
    phase = phase[::-1]                              # reverse the original phase
    next_phase = list(itertools.accumulate(phase))   # get the partial sum
    next_phase = [elem % 10 for elem in next_phase]  # keep only the unit digit
    return next_phase[::-1]                          # reverse again to create the next phase


def solve(phase):
    for i in range(100):
        phase = get_next_phase(phase)
    return get_digits(phase)


def parse(file_name):
    with open(file_name, "r") as f:
        input_str = f.readline().strip()

    offset = int(input_str[:7])
    signal_size = 10000 * len(input_str) - offset

    # keep only the last signal_size digits
    long_input_str = input_str
    while len(long_input_str) < signal_size:
        long_input_str += long_input_str
    long_input_str = long_input_str[len(long_input_str)-signal_size:]

    return [int(c) for c in long_input_str]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
