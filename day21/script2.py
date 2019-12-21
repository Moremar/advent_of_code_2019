from day21.script1 import parse, run_instructions


def solve(memory):

    # Rules to follow to not fall in a gap:
    # 1 - if A is a gap, jump
    # 2 - if B and C are ok, dont jump (it is useless and prevents us to jump on A, B or C)
    # 3 - if B or C is a gap, we jump if we are sure we will be able to jump twice, so if :
    #       * D and H are ok (jump/jump)
    #       * or D, E and I are ok (jump/walk/jump)
    #       * or D, E, F are ok (jump/walk/walk/jump)
    #
    # Translate in logical equation:
    # J = !A | [(!B | !C) & ([D & H] | [D & E & I] | [D & E & F])]
    # J = !A | [(!B | !C) & (D & (H | [E & I] | [E & F])]
    # J = !A | [(!B | !C) & (D & (H | [E & (I | F)])]
    #
    # Due to the constraint of having only 2 writable registers, we need to trick, because (!B or !C) and
    # (D & (H | [E & (I | F)]) both need 2 registers to calculate, so we negate the expression to get !J.
    # We will reverse it at the end by setting J to !J :
    # !J = A & [(B & C) | (!D | (!H & [!E | (!I & !F)])]
    #
    # To calculate (B & C), we would like something like :
    #  - copy B into T
    #  - then AND C T
    #
    # But we don't have a "copy" instruction, so we will use the property [B = (B or X) and B] for any X
    # This wil use one more instruction than with a copy, but we can get (B and C) with a single register by :
    #   OR B T
    #   AND B T
    #   AND C T
    #
    # This gives us the following instructions (exactly 15, how surprising...)

    instruction = "NOT I T\n" \
                  "NOT F J\n" \
                  "AND T J\n" \
                  "NOT E T\n" \
                  "OR T J\n" \
                  "NOT H T\n" \
                  "AND T J\n" \
                  "NOT D T\n" \
                  "OR T J\n" \
                  "OR B T\n" \
                  "AND B T\n" \
                  "AND C T\n" \
                  "OR T J\n" \
                  "AND A J\n" \
                  "NOT J J\n" \
                  "RUN\n"

    return run_instructions(memory, instruction)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
