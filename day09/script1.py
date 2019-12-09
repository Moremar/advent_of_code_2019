from day07.script1 import parse


def parse_opcode(token):
    """Extract the opcode and the mode of all params"""
    opcode = token % 100
    modes = [0, 0, 0, 0]
    if token > 100:
        for (i, mode) in enumerate(str(token)[-3::-1]):
            modes[i] = int(mode)
    return opcode, modes


class Program:
    """Object representation of the Intcode computer"""
    def __init__(self, memory, inputs, debug=False):
        self.memory = list(memory)
        self.instr_ptr = 0
        self.relative_base = 0
        self.inputs = inputs
        self.outputs = []
        self.completed = False
        self.stack = {}  # store memory outside of the size of memory
        self.count = 0  # count instructions (not used, just for debug)
        self.debug = debug

    def add_input(self, val):
        self.inputs.append(val)

    def write_value(self, position, to_write):
        if position < 0:
            raise ValueError("Negative address is not allowed.")
        elif position < len(self.memory):
            self.memory[position] = to_write
        else:
            self.stack[position] = to_write

    def read_value(self, position):
        if position < 0:
            raise ValueError("Negative address is not allowed.")
        elif position < len(self.memory):
            return self.memory[position]
        else:
            return self.stack[position] if position in self.stack else 0

    def param_value(self, position, mode):
        """Get the value of a param according to its mode"""
        if mode == 0:  # position mode
            return self.read_value(self.read_value(position))
        elif mode == 1:  # immediate mode
            return self.read_value(position)
        elif mode == 2:  # relative mode
            return self.read_value(self.read_value(position) + self.relative_base)
        else:
            raise ValueError("Unknown mode : ", mode)

    def run(self):
        """Run the program from where it last paused (from the start if first run)"""
        if self.completed:
            raise ValueError("Program already completed.")

        while True:
            self.count += 1
            (opcode, modes) = parse_opcode(self.memory[self.instr_ptr])
            if opcode == 99:  # Program end
                self.completed = True
                break

            elif opcode == 1:  # Addition
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                output_address = self.memory[self.instr_ptr + 3]
                if modes[2] == 2:
                    output_address += self.relative_base
                self.write_value(output_address, param1 + param2)

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Write {3} + {4} into memory[{5}]".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 4], modes,
                        param1, param2, output_address))

                self.instr_ptr += 4

            elif opcode == 2:  # Multiplication
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                output_address = self.memory[self.instr_ptr + 3]
                if modes[2] == 2:
                    output_address += self.relative_base
                self.write_value(output_address, param1 * param2)

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Write {3} * {4} into memory[{5}]".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 4], modes,
                        param1, param2, output_address))

                self.instr_ptr += 4

            elif opcode == 3:  # Store input in memory
                # if an input is available, use it, else pause the program
                if len(self.inputs) == 0:
                    break
                val_to_insert = self.inputs.pop(0)

                output_address = self.memory[self.instr_ptr + 1]
                if modes[0] == 2:
                    output_address += self.relative_base
                self.write_value(output_address, val_to_insert)

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Store input {3} into memory[{4}]".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 2], modes, val_to_insert,
                        output_address))

                self.instr_ptr += 2

            elif opcode == 4:  # Output a value
                val_to_output = self.param_value(self.instr_ptr + 1, modes[0])
                self.outputs.append(val_to_output)
                if self.debug:
                    print("{0}: {1} (mode {2}) -> Output {3}".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 2], modes, val_to_output))

                self.instr_ptr += 2

            elif opcode == 5:  # Jump if true
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Jump to {3} if {4} != 0".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 3], modes, param2, param1))

                if param1 != 0:
                    self.instr_ptr = param2
                else:
                    self.instr_ptr += 3

            elif opcode == 6:  # Jump if false
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Jump to {3} if {4} == 0".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 3], modes, param2, param1))

                if param1 == 0:
                    self.instr_ptr = param2
                else:
                    self.instr_ptr += 3

            elif opcode == 7:  # less than
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                output_address = self.memory[self.instr_ptr + 3]
                if modes[2] == 2:
                    output_address += self.relative_base
                self.write_value(output_address, 1 if param1 < param2 else 0)

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Writes {3} < {4} in {5}".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 4], modes, param1, param2,
                        output_address))

                self.instr_ptr += 4

            elif opcode == 8:  # Equals
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                param2 = self.param_value(self.instr_ptr + 2, modes[1])

                output_address = self.memory[self.instr_ptr + 3]
                if modes[2] == 2:
                    output_address += self.relative_base
                self.write_value(output_address, 1 if param1 == param2 else 0)

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Writes {3} = {4} in {5}".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 4], modes, param1, param2,
                        output_address))

                self.instr_ptr += 4

            elif opcode == 9:  # Update relative base
                param1 = self.param_value(self.instr_ptr + 1, modes[0])
                self.relative_base += param1

                if self.debug:
                    print("{0}: {1} (mode {2}) -> Add {3} to relative base".format(
                        self.count, self.memory[self.instr_ptr:self.instr_ptr + 2], modes, param1))

                self.instr_ptr += 2

            else:
                raise ValueError("Invalid opcode : ", opcode)


def solve(memory):
    program = Program(memory, [1])
    program.run()
    return program.outputs


if __name__ == '__main__':
    print(solve(parse("data.txt")))
