from day17.script1 import parse, Program, get_world, NORTH, EAST, SOUTH, WEST, DIRECTIONS

ASCII = {"A": 65, "B": 66, "C": 67, ",": 44, "R": 82, "L": 76, "n": 110, "y": 121,
         "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57}


def in_world(cell, world):
    return 0 <= cell[0] < len(world) and 0 <= cell[1] < len(world[0])


def get_cell(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def opposite(direction):
    return SOUTH if direction == NORTH \
        else NORTH if direction == SOUTH \
        else WEST if direction == EAST \
        else EAST


def turn_robot(robot_pos, robot_facing, world):
    for direction in DIRECTIONS:
        if direction == opposite(robot_facing) or direction == robot_facing:
            continue  # robot wont go backward not forward
        next_cell = get_cell(robot_pos, direction)
        if not in_world(next_cell, world):
            continue
        if world[next_cell[0]][next_cell[1]] == "#":
            # we either turn left or right
            if (DIRECTIONS.index(robot_facing) + 1) % 4 == DIRECTIONS.index(direction):
                return "R", direction
            else:
                return "L", direction
    # No more direction to go to, we walk all the walkable path
    return "", None


def get_path(world, robot_pos, robot_facing):
    full_path = ""
    (path, direction) = turn_robot(robot_pos, robot_facing, world)
    while direction is not None:
        full_path += path
        robot_facing = direction
        steps = 0
        next_cell = get_cell(robot_pos, direction)
        while in_world(next_cell, world) and world[next_cell[0]][next_cell[1]] == "#":
            steps += 1
            robot_pos = next_cell
            next_cell = get_cell(robot_pos, direction)
        full_path += str(steps)
        (path, direction) = turn_robot(robot_pos, robot_facing, world)
    return full_path


def get_routine(full_path):
    # Assume the 3 sequences have a size between 7 and 13 (since the commas are not counted yet)
    possible_seqs = []
    for i in range(7, 13):
        for j in range(0, len(full_path) - i + 1):
            possible_seq = full_path[j:j + i]
            if possible_seq not in possible_seqs:
                possible_seqs.append(possible_seq)

    for seq_a in possible_seqs:
        for seq_b in possible_seqs:
            if seq_b == seq_a:
                continue
            for seq_c in possible_seqs:
                if seq_c in [seq_a, seq_b]:
                    continue
                # try to create the path with these 3 seqs

                path = full_path
                routine = []
                while len(path) > 0:
                    if seq_a in path and path.index(seq_a) == 0:
                        routine.append("A")
                        path = path[len(seq_a):]
                    elif seq_b in path and path.index(seq_b) == 0:
                        routine.append("B")
                        path = path[len(seq_b):]
                    elif seq_c in path and path.index(seq_c) == 0:
                        routine.append("C")
                        path = path[len(seq_c):]
                    else:
                        break
                if len(path) == 0:
                    return routine, seq_a, seq_b, seq_c


def add_commas(seq):
    res = ""
    for i in range(len(seq)-1):
        res += seq[i]
        if seq[i] not in "0123456789" or seq[i+1] not in "0123456789":
            res += ","  # no comma between multi-digit numbers like "15"
    res += seq[-1]
    return res


def ascii_char(c):
    if c in ASCII:
        return ASCII[c]
    else:
        raise ValueError("No ASCII code for char ", c)


def ascii_array(s):
    return [ascii_char(c) for c in s]


def solve(memory):
    world, robot_pos, robot_facing = get_world(memory)

    # Find the path from start to end
    full_path = get_path(world, robot_pos, robot_facing)

    # Split it into a routine of 3 sequences
    routine, seq_a, seq_b, seq_c = get_routine(full_path)

    # run program with first memory set to 2 to give it the routine and the functions
    pgm = Program(memory, [])
    pgm.memory[0] = 2

    # Input the routine
    pgm.inputs += ascii_array(",".join(routine))
    pgm.inputs += [10]

    # Input the 3 sequences A, B and C
    pgm.inputs += ascii_array(add_commas(seq_a))
    pgm.inputs += [10]
    pgm.inputs += ascii_array(add_commas(seq_b))
    pgm.inputs += [10]
    pgm.inputs += ascii_array(add_commas(seq_c))
    pgm.inputs += [10]

    # Input the visual feedback
    pgm.inputs += ascii_array("n")
    pgm.inputs += [10]

    pgm.run()
    return pgm.outputs[-1]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
