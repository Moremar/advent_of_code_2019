import re


def process(curr, matches, limits):
    """Find recursively all 6-digits passwords with increasing digits
    and a sequence of 2 identical digits between the min and max limits"""
    if len(curr) == 6:
        if re.match(r".*(11|22|33|44|55|66|77|88|99).*", curr) and limits[0] <= curr <= limits[1]:
            matches.append(curr)
        return
    prev = int(curr[-1]) if len(curr) > 0 else 0
    for i in range(prev, 10):
        process(curr + str(i), matches, limits)


def solve(limits):
    matches = []
    process("", matches, limits)
    return len(matches)


def parse(file_name):
    """Parse the min and max limits of the password"""
    with open(file_name, "r") as f:
        match = re.match(r"(\d{6})-(\d{6})", f.readline())
        return (match.group(1), match.group(2))


if __name__ == '__main__':
    print(solve(parse("data.txt")))
