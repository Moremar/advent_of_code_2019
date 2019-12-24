class World:
    def __init__(self):
        self.levels = {}

    def get(self, i, j, level):
        return self.levels[level][(i, j)] if level in self.levels else 0

    def set(self, i, j, level, val):
        if level not in self.levels:
            self.levels[level] = {}
        self.levels[level][(i, j)] = val

    def print(self):
        for k in sorted(list(self.levels.keys())):
            world_str = "Level " + str(k) + ":\n"
            for j in range(5):
                for i in range(5):
                    world_str += "?" if (i, j) == (2, 2) else "#" if self.levels[k][(i, j)] == 1 else "."
                world_str += "\n"
            print(world_str)

    def trim(self):
        """Remove the lowest and biggest levels if there are no bug in them"""
        level_ids = sorted(list(self.levels.keys()))
        k = level_ids[0]
        while k < 0 and sum(self.levels[k][coords] for coords in self.levels[k]) == 0:
            del self.levels[k]
            k += 1
        k = level_ids[-1]
        while k > 0 and sum(self.levels[k][coords] for coords in self.levels[k]) == 0:
            del self.levels[k]
            k -= 1

    def count_adj(self, i, j, level):
        adj = 0
        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
        for (x, y) in neighbors:
            # handle cases one level below
            if x == -1:
                adj += self.get(1, 2, level - 1)
            elif x == 5:
                adj += self.get(3, 2, level - 1)
            elif y == -1:
                adj += self.get(2, 1, level - 1)
            elif y == 5:
                adj += self.get(2, 3, level - 1)
            # handle cases one level above
            elif (x, y) == (2, 2):
                if i == 1:
                    adj += sum([self.get(0, j1, level + 1) for j1 in range(5)])
                elif i == 3:
                    adj += sum([self.get(4, j1, level + 1) for j1 in range(5)])
                elif j == 1:
                    adj += sum([self.get(i1, 0, level + 1) for i1 in range(5)])
                elif j == 3:
                    adj += sum([self.get(i1, 4, level + 1) for i1 in range(5)])
            # handle cases with no interaction with other levels
            else:
                adj += self.get(x, y, level)
        return adj

    def count_bugs(self):
        return sum([sum([self.get(i, j, k) for (i, j) in self.levels[k]]) for k in self.levels])

    def get_next_step(self):
        next_world = World()
        # The next level can have up to 1 more level above and below
        next_levels = sorted(list(self.levels.keys()))
        next_levels.insert(0, next_levels[0] - 1)
        next_levels.append(next_levels[-1] + 1)
        for k in next_levels:
            for i in range(5):
                for j in range(5):
                    if (i, j) == (2, 2):
                        next_world.set(i, j, k, 0)
                        continue
                    adj = self.count_adj(i, j, k)
                    if self.get(i, j, k) == 1 and adj != 1:
                        next_world.set(i, j, k, 0)
                    elif self.get(i, j, k) == 0 and 1 <= adj <= 2:
                        next_world.set(i, j, k, 1)
                    else:
                        next_world.set(i, j, k, self.get(i, j, k))
        next_world.trim()
        return next_world


def solve(world):
    world.print()
    for turn in range(200):
        world = world.get_next_step()
        # world.print()
    return world.count_bugs()


def parse(file_name):
    world = World()
    with open(file_name, "r") as f:
        for (j, line) in enumerate([line.strip() for line in f.readlines()]):
            for (i, c) in enumerate(line):
                world.set(i, j, 0, 1 if c == "#" else 0)
    return world


if __name__ == '__main__':
    print(solve(parse("data.txt")))
