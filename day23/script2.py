from day23.script1 import parse, Program


class Nat:
    def __init__(self):
        self.x = None
        self.y = None
        self.sent = []

    def update(self, x, y):
        self.x = x
        self.y = y


def solve(memory):
    pgms = [Program(list(memory), [i, -1]) for i in range(50)]
    nat = Nat()
    while True:
        trigger_nat = True
        for i in range(50):
            pgms[i].run()
            while len(pgms[i].outputs) > 0:
                trigger_nat = False  # one machine at least is not idle
                dest = pgms[i].outputs.pop(0)
                x = pgms[i].outputs.pop(0)
                y = pgms[i].outputs.pop(0)
                if dest == 255:
                    nat.update(x, y)
                else:
                    pgms[dest].inputs += [x, y]
            pgms[i].inputs.append(-1)

        if trigger_nat:
            if nat.y in nat.sent:
                return nat.y
            else:
                nat.sent.append(nat.y)
            pgms[0].inputs += [nat.x, nat.y]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
