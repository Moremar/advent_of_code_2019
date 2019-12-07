from day05.script2 import parse, param_value, parse_opcode


class Program:
    """Object representation of the Intcode computer"""
    def __init__(self, memory, inputs):
        self.memory = list(memory)
        self.instr_ptr = 0
        self.inputs = inputs
        self.outputs = []
        self.completed = False

    def add_input(self, val):
        self.inputs.append(val)

    def run(self):
        """Run the program from where it last paused (from the start if first run)"""
        if self.completed:
            raise ValueError("Program already completed.")

        while True:
            (opcode, modes) = parse_opcode(self.memory[self.instr_ptr])
            if opcode == 99:  # Program end
                self.completed = True
                break

            elif opcode in [1, 2]:  # 1 = Addition, 2 = Multiplication
                param1 = param_value(self.memory, self.instr_ptr + 1, modes[0])
                param2 = param_value(self.memory, self.instr_ptr + 2, modes[1])
                output_address = self.memory[self.instr_ptr + 3]
                self.memory[output_address] = (param1 + param2) if opcode == 1 else (param1 * param2)
                # move forward the instruction pointer
                self.instr_ptr += 4

            elif opcode == 3:  # Store input in memory
                # if an input is available, use it, else pause the program
                if len(self.inputs) == 0:
                    break
                val_to_insert = self.inputs.pop(0)
                output_address = self.memory[self.instr_ptr + 1]
                self.memory[output_address] = val_to_insert
                self.instr_ptr += 2

            elif opcode == 4:  # Output a value
                val_to_output = param_value(self.memory, self.instr_ptr + 1, modes[0])
                self.outputs.append(val_to_output)
                self.instr_ptr += 2

            elif opcode == 5:  # Jump if true
                param1 = param_value(self.memory, self.instr_ptr + 1, modes[0])
                if param1 != 0:
                    self.instr_ptr = param_value(self.memory, self.instr_ptr + 2, modes[1])
                else:
                    self.instr_ptr += 3

            elif opcode == 6:  # Jump if false
                param1 = param_value(self.memory, self.instr_ptr + 1, modes[0])
                if param1 == 0:
                    self.instr_ptr = param_value(self.memory, self.instr_ptr + 2, modes[1])
                else:
                    self.instr_ptr += 3

            elif opcode == 7:  # less than
                param1 = param_value(self.memory, self.instr_ptr + 1, modes[0])
                param2 = param_value(self.memory, self.instr_ptr + 2, modes[1])
                output_address = self.memory[self.instr_ptr + 3]
                self.memory[output_address] = 1 if param1 < param2 else 0
                self.instr_ptr += 4

            elif opcode == 8:  # Equals
                param1 = param_value(self.memory, self.instr_ptr + 1, modes[0])
                param2 = param_value(self.memory, self.instr_ptr + 2, modes[1])
                output_address = self.memory[self.instr_ptr + 3]
                self.memory[output_address] = 1 if param1 == param2 else 0
                self.instr_ptr += 4

            else:
                raise ValueError("Invalid opcode : ", opcode)


def compute_permutations(prev, items, result):
    if len(items) == 0:
        result.append(prev)
    for i in range(0, len(items)):
        rest = list(items)
        item = rest.pop(i)
        compute_permutations(prev + [item], rest, result)


def get_permutations(items):
    permutations = []
    compute_permutations([], items, permutations)
    return permutations


def solve(memory):
    best_signal = 0
    for permutation in get_permutations([0, 1, 2, 3, 4]):
        amp1 = Program(memory, [permutation[0], 0])
        amp1.run()
        amp2 = Program(memory, [permutation[1], amp1.outputs.pop(0)])
        amp2.run()
        amp3 = Program(memory, [permutation[2], amp2.outputs.pop(0)])
        amp3.run()
        amp4 = Program(memory, [permutation[3], amp3.outputs.pop(0)])
        amp4.run()
        amp5 = Program(memory, [permutation[4], amp4.outputs.pop(0)])
        amp5.run()

        signal = amp5.outputs.pop(0)
        if signal > best_signal:
            best_signal = signal
    return best_signal


if __name__ == '__main__':
    print(solve(parse("data.txt")))
