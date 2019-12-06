import re


class Planet:
    def __init__(self, name, orbit_around):
        self.name = name
        self.orbit_around = orbit_around
        self.orbited_by = []


def solve(planets):
    orbits = 0
    for planet_name in planets:
        curr_planet_name = planet_name
        while planets[curr_planet_name].orbit_around is not None:
            orbits += 1
            curr_planet_name = planets[curr_planet_name].orbit_around
    return orbits


def parse(file_name):
    planets = {}
    with open(file_name, "r") as f:
        for line in f.readlines():
            match = re.match(r"(.*)\)(.*)", line)
            (origin, satellite) = (match.group(1), match.group(2))
            if origin not in planets:
                planets[origin] = Planet(origin, None)
            if satellite not in planets:
                planets[satellite] = Planet(satellite, origin)
            else:
                # satellite was already found as a source but not as a satellite
                planets[satellite].orbit_around = origin
            if satellite not in planets[origin].orbited_by:
                planets[origin].orbited_by.append(satellite)
    return planets


if __name__ == '__main__':
    print(solve(parse("data.txt")))

