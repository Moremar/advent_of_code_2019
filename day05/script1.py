
def parse_opcode(token):
    """Extract the opcode and the mode of all params"""
    opcode = token % 100
    modes = [0, 0, 0, 0]
    if token > 100:
        for (i, mode) in enumerate(str(token)[-3::-1]):
            modes[i] = int(mode)
    return opcode, modes


def param_value(memory, position, mode):
    """Get the value of a param according to its mode"""
    if mode == 0:  # position mode
        return memory[memory[position]]
    elif mode == 1: # immediate mode
        return memory[position]
    else:
        raise ValueError("Unknown mode : ", mode)


def run_program(memory, inputs):
    """Execute the successive instructions of the program"""
    instr_ptr = 0
    output = []

    while True:
        (opcode, modes) = parse_opcode(memory[instr_ptr])

        if opcode == 99:  # Program end
            break

        elif opcode in [1, 2]:  # 1 = Addition, 2 = Multiplication
            param1 = param_value(memory, instr_ptr + 1, modes[0])
            param2 = param_value(memory, instr_ptr + 2, modes[1])
            output_address = memory[instr_ptr + 3]
            memory[output_address] = (param1 + param2) if opcode == 1 else (param1 * param2)
            # move forward the instruction pointer
            instr_ptr += 4

        elif opcode == 3:  # Store input in memory (program init)
            val_to_insert = inputs.pop(0)
            output_address = memory[instr_ptr + 1]
            memory[output_address] = val_to_insert
            instr_ptr += 2

        elif opcode == 4:  # Output a value
            val_to_output = param_value(memory, instr_ptr + 1, modes[0])
            output.append(val_to_output)
            instr_ptr += 2

        else:
            raise ValueError("Invalid opcode : ", opcode)
    return output


def solve(memory):
    """Return the last value of the output"""
    return run_program(memory, [1])[-1]


def parse(file_name):
    """Parse the data file into a list of int"""
    with open(file_name, "r") as f:
        return [int(x) for x in f.readline().split(",")]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
