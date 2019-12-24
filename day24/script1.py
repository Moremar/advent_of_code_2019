from math import pow


class World:
    def __init__(self):
        self.state = {}

    def count_adj(self, i, j):
        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        return sum([self.state[(x, y)] for (x, y) in neighbors if (x, y) in self.state])

    def get(self, i, j):
        return self.state[(i, j)]

    def set(self, i, j, val):
        self.state[(i, j)] = val

    def get_next_step(self):
        next_world = World()
        for i in range(5):
            for j in range(5):
                adj = self.count_adj(i, j)
                if self.get(i, j) == 1 and adj != 1:
                    next_world.set(i, j, 0)
                elif self.get(i, j) == 0 and 1 <= adj <= 2:
                    next_world.set(i, j, 1)
                else:
                    next_world.set(i, j, self.get(i, j))
        return next_world

    def print(self):
        world_str = ""
        for j in range(5):
            for i in range(5):
                world_str += "#" if self.get(i, j) == 1 else "."
            world_str += "\n"
        print(world_str)

    def calculate_bio(self):
        return sum([pow(2, j * 5 + i) for (i, j) in self.state if self.get(i, j) == 1])


def solve(world):
    states = [dict(world.state)]
    world.print()
    while True:
        world = world.get_next_step()
        if world.state in states:
            world.print()
            return world.calculate_bio()
        else:
            states.append(dict(world.state))


def parse(file_name):
    world = World()
    with open(file_name, "r") as f:
        for (j, line) in enumerate([line.strip() for line in f.readlines()]):
            for (i, c) in enumerate(line):
                world.set(i, j, 1 if c == "#" else 0)
    return world


if __name__ == '__main__':
    print(solve(parse("data.txt")))
