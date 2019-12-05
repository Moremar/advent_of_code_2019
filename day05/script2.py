from day05.script1 import parse, parse_opcode, param_value


def run_program(memory, system_id):
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
            val_to_insert = system_id
            output_address = memory[instr_ptr + 1]
            memory[output_address] = val_to_insert
            instr_ptr += 2

        elif opcode == 4:  # Output a value
            val_to_output = param_value(memory, instr_ptr + 1, modes[0])
            output.append(val_to_output)
            instr_ptr += 2

        elif opcode == 5:  # Jump if true
            param1 = param_value(memory, instr_ptr + 1, modes[0])
            if param1 != 0:
                instr_ptr = param_value(memory, instr_ptr + 2, modes[1])
            else:
                instr_ptr += 3

        elif opcode == 6:  # Jump if false
            param1 = param_value(memory, instr_ptr + 1, modes[0])
            if param1 == 0:
                instr_ptr = param_value(memory, instr_ptr + 2, modes[1])
            else:
                instr_ptr += 3

        elif opcode == 7:  # less than
            param1 = param_value(memory, instr_ptr + 1, modes[0])
            param2 = param_value(memory, instr_ptr + 2, modes[1])
            output_address = memory[instr_ptr + 3]
            memory[output_address] = 1 if param1 < param2 else 0
            instr_ptr += 4

        elif opcode == 8:  # Equals
            param1 = param_value(memory, instr_ptr + 1, modes[0])
            param2 = param_value(memory, instr_ptr + 2, modes[1])
            output_address = memory[instr_ptr + 3]
            memory[output_address] = 1 if param1 == param2 else 0
            instr_ptr += 4

        else:
            raise ValueError("Invalid opcode : ", opcode)
    return output


def solve(memory):
    # return last output
    return run_program(memory, 5)[-1]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
