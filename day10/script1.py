from math import inf


def find_station_meteor(meteors):
    # Find the meteor from which we can see the biggest number of other meteors
    # If some meteors are hidden, they will share the same direction with a visible one
    # For a given direction, we need to distinguish left and right (since from the station we can see
    # up to one meteor on each side)

    max_meteors_in_sight = 0
    best_meteor = (0, 0)
    for meteor1 in meteors:
        directions = {}
        for meteor2 in meteors:
            if meteor1 == meteor2:
                continue
            if meteor2[0] == meteor1[0]:
                direction = ("L_" if meteor2[1] > meteor1[1] else "R_") + str(inf)
            else:
                direction = (meteor2[1] - meteor1[1]) / (meteor2[0] - meteor1[0])
                direction = ("L_" if meteor2[0] < meteor1[0] else "R_") + str(direction)
            directions[direction] = 1
        if len(directions) > max_meteors_in_sight:
            max_meteors_in_sight = len(directions)
            best_meteor = meteor1

    return max_meteors_in_sight, best_meteor


def solve(meteors):
    return find_station_meteor(meteors)[0]


def parse(file_name):
    with open(file_name, "r") as f:
        meteors = []
        for (j, line) in enumerate([l.strip() for l in f.readlines()]):
            for i in range(0, len(line)):
                if line[i] == "#":
                    meteors.append((i, j))
        return meteors


if __name__ == '__main__':
    print(solve(parse("data.txt")))
