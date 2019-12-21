from day17.script1 import parse, Program

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "abcdefghijklmnopqrstuvwxyz"

ASCII_TO_CODE = {" ": 32, "\n": 10, "#": 35, "@": 64, ".": 46, ":": 58, "'": 39}
for (i, letter) in enumerate(ALPHABET):
    ASCII_TO_CODE[letter] = i + 65
for (i, letter) in enumerate(alphabet):
    ASCII_TO_CODE[letter] = i + 97

CODE_TO_ASCII = {}
for (k, v) in ASCII_TO_CODE.items():
    CODE_TO_ASCII[v] = k


def to_ascii(code_array):
    return "".join([CODE_TO_ASCII[code] for code in code_array])


def to_codes(s):
    return [ASCII_TO_CODE[c] for c in s]


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
