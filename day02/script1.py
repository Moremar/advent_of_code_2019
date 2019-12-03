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
            # opcode 1 is addition, opcode 2 is multiplication
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
    """Run the program and get the value in the address 0"""
    memory = init_memory(original, 12, 2)
    run_program(memory)
    return memory[0]


def parse(file_name):
    """Parse the data file into a sequence of integers"""
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
