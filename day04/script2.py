from day04.script1 import parse, process
from collections import Counter   # Counter("aba") = {"a": 2, "b": 1 }


def solve(limits):
    matches = []
    process("", matches, limits)

    # all digits are in order so all occurrences of a digit are grouped together
    # we just need to count the occurrences of all digits and check if a digit has 2 occurrences
    valid = [match for match in matches if 2 in Counter(match).values()]
    return len(valid)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
