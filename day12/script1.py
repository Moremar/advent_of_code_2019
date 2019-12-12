import re


class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x, self.y, self.z = (x, y, z)
        self.vx, self.vy, self.vz = (vx, vy, vz)

    def __repr__(self):
        return "Moon({0}, {1}, {2}, {3}, {4}, {5})".format(self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def copy(self):
        return Moon(self.x, self.y, self.z, self.vx, self.vy, self.vz)


def sign_diff(a, b):
    return 1 if a < b else -1 if a > b else 0


def step(moons):
    moons_after = []
    for moon in moons:
        moon_after = moon.copy()
        for moon2 in moons:
            if moon == moon2:
                continue
            moon_after.vx += sign_diff(moon.x, moon2.x)
            moon_after.vy += sign_diff(moon.y, moon2.y)
            moon_after.vz += sign_diff(moon.z, moon2.z)
        moon_after.x += moon_after.vx
        moon_after.y += moon_after.vy
        moon_after.z += moon_after.vz
        moons_after.append(moon_after)
    return moons_after


def total_energy(moons):
    energy = 0
    for moon in moons:
        potential = abs(moon.x) + abs(moon.y) + abs(moon.z)
        kinectic = abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
        energy += potential * kinectic
    return energy


def solve(moons):
    for i in range(0, 1000):
        moons = step(moons)
    return total_energy(moons)


def parse(file_name):
    moons = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            _, x, y, z, _ = re.split(r"<x=([-0-9]+), y=([-0-9]+), z=([-0-9]+)>", line)
            moons.append(Moon(int(x), int(y), int(z)))
    return moons


if __name__ == '__main__':
    print(solve(parse("data.txt")))
