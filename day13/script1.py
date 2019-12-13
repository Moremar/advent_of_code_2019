from day13.program import Program


def solve(pgm):
    pgm.run()
    tile_ids = [pgm.outputs[i] for i in range(len(pgm.outputs)) if i % 3 == 2]
    return tile_ids.count(2)


def parse(file_name):
    with open(file_name, "r") as f:
        memory = [int(x) for x in f.readline().strip().split(",")]
        return Program(memory, [])


if __name__ == '__main__':
    print(solve(parse("data.txt")))
