from math import floor


def fuel_for_module(mass):
    """Fuel required for a given mass"""
    return floor(mass / 3) - 2


def solve(data):
    """Compute the total fuel requirement"""
    return sum([fuel_for_module(mass) for mass in data])


def parse(file_name):
    """Parse the data file"""
    with open(file_name, "r") as f:
        return [int(line) for line in f.readlines()]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
