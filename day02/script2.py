def init_memory(original, noun, verb):
    """Return a copy of the original memory state with the custom noun and verb"""
    return [original[0], noun, verb] + original[3:]


def run_program(memory):
    """Execute the successive instructions of the program"""
    instr_ptr = 0
    while True:
        opcode = memory[instr_ptr]
        if opcode == 99:
            # opcode 99 means the program is completed
            break
        elif opcode in [1, 2]:
            param1 = memory[memory[instr_ptr + 1]]
            param2 = memory[memory[instr_ptr + 2]]
            output_address = memory[instr_ptr + 3]
            memory[output_address] = (param1 + param2) if opcode == 1 else (param1 * param2)
            # move forward the instruction pointer
            instr_ptr += 4
        else:
            raise ValueError("Invalid opcode : ", opcode)
    return memory


def solve(original):
    """Find the (noun, verb) pair that generates the expected output in the address 0"""
    for noun in range(0, 100):
        for verb in range(0, 100):
            memory = init_memory(original, noun, verb)
            run_program(memory)
            if memory[0] == 19690720:
                return 100 * noun + verb
    raise ValueError("No (noun, verb) pair returned the expected output.")


def parse(file_name):
    """Parse the data file into a list of integers"""
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
