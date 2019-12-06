from day06.script1 import parse


def solve(planets):
    processed = []
    to_process = [("YOU", 0)]
    while len(to_process) > 0:
        (planet_name, distance) = to_process.pop(0)
        if planet_name in processed:
            continue
        planet = planets[planet_name]
        adjacents = planet.orbited_by + [planet.orbit_around]
        if "SAN" in adjacents:
            return distance - 1  # -1 because we want the distance to the planet before SAN
        for adjacent in adjacents:
            if adjacent not in processed and adjacent is not None:
                to_process.append((adjacent, distance + 1))
        processed.append(planet_name)
    raise ValueError("No orbital route was found from YOU to SAN")


if __name__ == '__main__':
    print(solve(parse("data.txt")))
