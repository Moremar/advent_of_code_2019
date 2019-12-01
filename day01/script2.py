from math import floor


def fuel_required(mass):
    """Fuel required for a given mass"""
    return floor(mass / 3) - 2


def fuel_for_fuel(mass):
    """Fuel required for a given mass of fuel (calculated recursively)"""
    fuel = 0
    fuel_delta = fuel_required(mass)
    while 0 < fuel_delta:
        fuel += fuel_delta
        fuel_delta = fuel_required(fuel_delta)
    return fuel


def fuel_for_module(mass):
    # The fuel required by a module is the sum of the fuel required by its mass
    # and the fuel required by the mass of this fuel (calculated recursively)
    fuel_module = fuel_required(mass)
    fuel_fuel = fuel_for_fuel(fuel_module)
    return fuel_module + fuel_fuel


def solve(data):
    """Compute the total fuel requirement"""
    return sum([fuel_for_module(mass) for mass in data])


def parse(file_name):
    """Parse the input file"""
    with open(file_name, "r") as f:
        return [int(line) for line in f.readlines()]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
