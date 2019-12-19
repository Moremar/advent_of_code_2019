from day13.script1 import Program

WORLD_SIZE = 50


def is_in_beam(memory, x, y):
    pgm = Program(list(memory), [])
    pgm.inputs += [x, y]
    pgm.run()
    return pgm.outputs[0] == 1


def get_world(memory):
    world = [[0] * WORLD_SIZE for _ in range(WORLD_SIZE)]
    for y in range(WORLD_SIZE):
        for x in range(WORLD_SIZE):
            world[y][x] = 1 if is_in_beam(memory, x, y) else 0
    return world


def solve(memory):
    world = get_world(memory)
    return sum([sum(line) for line in world])


def parse(file_name):
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().strip().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
