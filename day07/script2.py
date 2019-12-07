from day07.script1 import parse, get_permutations, Program


def solve(memory):
    highest = 0
    for permutation in get_permutations([5, 6, 7, 8, 9]):
        amp1 = Program(memory, [permutation[0], 0])
        amp2 = Program(memory, [permutation[1]])
        amp3 = Program(memory, [permutation[2]])
        amp4 = Program(memory, [permutation[3]])
        amp5 = Program(memory, [permutation[4]])

        while not amp5.completed:
            amp1.run()
            amp2.add_input(amp1.outputs.pop(0))
            amp2.run()
            amp3.add_input(amp2.outputs.pop(0))
            amp3.run()
            amp4.add_input(amp3.outputs.pop(0))
            amp4.run()
            amp5.add_input(amp4.outputs.pop(0))
            amp5.run()
            output5 = amp5.outputs.pop(0)
            if not amp5.completed:
                amp1.add_input(output5)
            elif output5 > highest:
                highest = output5
    return highest


if __name__ == '__main__':
    print(solve(parse("data.txt")))
