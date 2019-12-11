from day11.script1 import parse, play_bot


def pretty_print(world):
    xs = [x for (x, _) in world]
    ys = [y for (_, y) in world]
    result = ""
    for y in range(max(ys), min(ys)-1, -1):
        for x in range(min(xs), max(xs) + 1):
            result += "#" if (x, y) in world and world[(x, y)] == 1 else " "
        result += "\n"
    return result


def solve(memory):
    world = {(0, 0): 1}
    play_bot(world, memory)
    return pretty_print(world)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
