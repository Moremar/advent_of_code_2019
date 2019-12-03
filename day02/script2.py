from day02.script1 import parse, init_memory, run_program


def solve(original):
    """Find the (noun, verb) pair that generates the expected output in the address 0"""
    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = init_memory(original, noun, verb)
            run_program(memory)
            if memory[0] == 19690720:
                return 100 * noun + verb
    raise ValueError("No (noun, verb) pair returned the expected output.")


if __name__ == '__main__':
    print(solve(parse("data.txt")))
