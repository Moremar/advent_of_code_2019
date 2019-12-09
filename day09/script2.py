from day09.script1 import parse, Program


def solve(memory):
    program = Program(memory, [2])
    program.run()
    return program.outputs


if __name__ == '__main__':
    print(solve(parse("data.txt")))
