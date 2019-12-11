from day09.script1 import parse, Program

UP, RIGHT, DOWN, LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)


def get_next_dir(facing, dir_input):
    directions = [UP, RIGHT, DOWN, LEFT]
    next_dir = directions[(directions.index(facing) + (-1 if dir_input == 0 else 1)) % 4]
    return next_dir


def play_bot(world, memory):
    robot_pos = (0, 0)
    robot_facing = UP
    program = Program(memory, [])
    while not program.completed:
        program.run()
        # perform all the moves provided in output
        while len(program.outputs) > 0:
            color = program.outputs.pop(0)
            dir_input = program.outputs.pop(0)
            world[robot_pos] = color
            robot_facing = get_next_dir(robot_facing, dir_input)
            robot_pos = (robot_pos[0] + robot_facing[0], robot_pos[1] + robot_facing[1])
        # provide an input
        program.inputs.append(world[robot_pos] if robot_pos in world else 0)


def solve(memory):
    world = {}
    play_bot(world, memory)
    return len(world)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
