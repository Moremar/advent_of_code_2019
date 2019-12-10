from day10.script1 import parse, find_station_meteor
from math import sqrt, pow, inf

# decorator to let us write only __lt__, __eq__ and __ne__ and auto-implement other comparison functions
from functools import total_ordering


@total_ordering
class Direction:
    # global variable for the position of the station
    station = None

    def __init__(self, coef, side):
        self.coef = coef
        self.side = side  # 0 for right, 1 for left
        self.meteors = []

    def __repr__(self):
        return "Direction(" + str(self.side) + ", " + str(self.coef) + ", " + str(self.meteors) + ")"

    def __eq__(self, other):
        return self.coef == other.coef and self.side == other.side

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        # Custom order to have the directions in order or vaporization
        if self.side == "RIGHT" and other.side == "LEFT":
            return True
        elif self.side == "LEFT" and other.side == "RIGHT":
            return False
        elif self.side == "RIGHT" and other.side == "RIGHT":
            return self.coef < other.coef
        else:
            return self.coef < other.coef

    def add_meteor(self, meteor):
        self.meteors.append(meteor)

    def vaporize(self):
        # vaporize the closest meteor from the station in this direction
        min_dist = inf
        min_meteor = None
        for meteor in self.meteors:
            distance = sqrt(pow(meteor[0]-Direction.station[0], 2) + pow(meteor[0] - Direction.station[1], 2))
            if distance < min_dist:
                min_meteor = meteor
                min_dist = distance
        self.meteors.remove(min_meteor)
        return min_meteor


def solve(meteors, to_frag):
    station = find_station_meteor(meteors)[1]
    Direction.station = station

    # compute the direction of all meteors from the station
    directions = []
    for meteor in meteors:
        if station == meteor:
            continue
        if meteor[0] == station[0]:
            meteor_dir = Direction(-inf, "RIGHT" if meteor[1] < station[1] else "LEFT")
        else:
            meteor_dir = Direction((meteor[1] - station[1]) / (meteor[0] - station[0]),
                                   "RIGHT" if meteor[0] > station[0] else "LEFT")

        # if there is already a meteor in this direction, add this new one, else create the direction
        if meteor_dir in directions:
            directions[directions.index(meteor_dir)].add_meteor(meteor)
        else:
            meteor_dir.add_meteor(meteor)
            directions.append(meteor_dir)

    # sort directions in vaporization order
    directions.sort()

    # vaporize meteors one by one
    direction_index = 0
    while True:
        vaporized = directions[direction_index].vaporize()
        to_frag -= 1
        direction_index += 1
        if to_frag == 0:
            return vaporized[0] * 100 + vaporized[1]

        # clean the empty directions after a 360 degrees shot
        if direction_index == len(directions):
            directions = [direction for direction in directions if len(direction.meteors) > 0]
            direction_index = 0

        if len(directions) == 0 and to_frag > 0:
            raise ValueError("Not enough meteors to vaporize.")


if __name__ == '__main__':
    print(solve(parse("data.txt"), 200))
