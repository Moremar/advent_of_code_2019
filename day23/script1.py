from day13.script1 import Program


def solve(memory):
    pgms = [Program(list(memory), [i, -1]) for i in range(50)]
    while True:
        for i in range(50):
            pgms[i].run()
            while len(pgms[i].outputs) > 0:
                dest = pgms[i].outputs.pop(0)
                x = pgms[i].outputs.pop(0)
                y = pgms[i].outputs.pop(0)
                if dest == 255:
                    return y
                pgms[dest].inputs += [x, y]
            pgms[i].inputs.append(-1)


def parse(file_name):
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().strip().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
