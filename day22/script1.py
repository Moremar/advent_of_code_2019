import re

DECK_SIZE = 10007


class Technique:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __repr__(self):
        return "Tech({0}, {1})".format(self.name, self.count)


def apply_technique(position, technique):
    if technique.name == "new stack":
        return (DECK_SIZE - 1) - position
    elif technique.name == "cut":
        return (position - technique.count) % DECK_SIZE
    else:
        return (position * technique.count) % DECK_SIZE


def shuffle(position, techniques):
    for technique in techniques:
        position = apply_technique(position, technique)
        print("# ", position, " after ", technique)
    return position


def solve(techniques):
    return shuffle(2019, techniques)


def parse(file_name):
    techniques = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            if "cut" in line:
                _, technique, count, _ = re.split(r"^(cut) ([-0-9]+)", line)
            elif "deal into new stack" in line:
                technique, count = "new stack", "0"
            elif "increment" in line:
                _, technique, count, _ = re.split(r"^(deal with increment) ([0-9]+)", line)
            else:
                raise ValueError("Unknown technique: ", line)
            techniques.append(Technique(technique, int(count)))
    return techniques


if __name__ == '__main__':
    print(solve(parse("data.txt")))
