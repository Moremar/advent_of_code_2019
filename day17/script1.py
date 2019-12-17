from day13.script1 import Program

NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)  # with i distance to left and j to top
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


def get_world(memory):
    pgm = Program(memory, [])
    pgm.run()
    world_i = pgm.outputs.index(10)
    world_j = pgm.outputs.count(10) - 1  # -1 because last output is a newline
    world = [["?"] * world_i for _ in range(world_j)]
    (j, i) = (0, 0)
    (robot_pos, robot_facing) = (None, None)
    while len(pgm.outputs) > 0:
        ascii_val = pgm.outputs.pop(0)
        if ascii_val == 10:
            (j, i) = (j + 1, 0)
            continue
        elif ascii_val == 46:
            world[j][i] = "."
        elif ascii_val == 35:
            world[j][i] = "#"
        elif ascii_val == 94:
            world[j][i] = "#"
            robot_pos = (j, i)
            robot_facing = NORTH
        else:
            raise ValueError("ASCII not supported: ", ascii_val)
        i += 1
    return world, robot_pos, robot_facing


def solve(memory):
    world, _, _ = get_world(memory)

    # Count intersections
    align_param_sum = 0
    for i in range(1, len(world[0])-1):
        for j in range(1, len(world)-1):
            if world[j][i] == "#" and world[j][i-1] == "#" and world[j][i+1] == "#" \
                    and world[j-1][i] == "#" and world[j+1][i] == "#":
                align_param_sum += i * j
    return align_param_sum


def parse(file_name):
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().strip().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
