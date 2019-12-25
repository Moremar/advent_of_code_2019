from day17.script1 import parse, Program


def to_ascii(code_array):
    """String corresponding to an array of ASCII codes"""
    return "".join([chr(code) for code in code_array])


def to_codes(s):
    """Array of ASCII codes corresponding to a string"""
    return [ord(c) for c in s]


def run_instructions(memory, instructions):
    pgm = Program(memory, to_codes(instructions))
    pgm.run()
    print(to_ascii(pgm.outputs[:-1]))
    return pgm.outputs[-1]


def solve(memory):

    # Rules :
    # 1 - if D is a gap, dont jump
    # 2 - if all next 3 tiles are ok, dont jump (it would be useless and prevent us to jump from A, B or C)
    #
    # Translate into equation:
    # J = D & (!A | !B | !C)

    instructions = "NOT A T\n" \
                  "NOT B J\n" \
                  "OR T J\n" \
                  "NOT C T\n" \
                  "OR T J\n" \
                  "AND D J\n" \
                  "WALK\n"

    return run_instructions(memory, instructions)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
