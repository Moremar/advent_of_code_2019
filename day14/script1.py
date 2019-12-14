from math import ceil


class Reaction:
    def __init__(self, chemical_in, chemical_out):
        self.chemical_in = chemical_in
        self.chemical_out = chemical_out


def produce_fuel(reactions, reserve):
    fuel_reac = [r for r in reactions if r.chemical_out[0] == "FUEL"][0]
    to_produce = list(fuel_reac.chemical_in)
    cost = 0
    while len(to_produce) > 0:
        producing = to_produce.pop(0)

        if producing[0] == "ORE":
            cost += producing[1]
            continue

        if producing[0] in reserve:
            if producing[1] <= reserve[producing[0]]:
                # we have already enough components available in reserve
                reserve[producing[0]] -= producing[1]
                continue
            else:
                # we have some components in reserve but not enough
                producing = (producing[0], producing[1] - reserve[producing[0]])
                del reserve[producing[0]]

        # find the reaction to generate the component and apply it as many times as needed
        reac = [r for r in reactions if r.chemical_out[0] == producing[0]][0]
        times_to_apply = ceil(producing[1] / reac.chemical_out[1])
        reserve[producing[0]] = times_to_apply * reac.chemical_out[1] - producing[1]

        # add the chemical inputs of the reaction we just applied in the compoennts to produce
        for component in reac.chemical_in:
            to_produce.append((component[0], times_to_apply * component[1]))

    return cost


def solve(reactions):
    return produce_fuel(reactions, {})


def parse(file_name):
    reactions = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            (inputs, output) = line.split("=>")
            (quantity, name) = output.strip().split(" ")
            chemical_out = (name, int(quantity.strip()))
            chemical_in = []
            for elem in inputs.split(", "):
                (quantity, name) = elem.strip().split(" ")
                chemical_in.append((name, int(quantity.strip())))
            reactions.append(Reaction(chemical_in, chemical_out))
        return reactions


if __name__ == '__main__':
    print(solve(parse("data.txt")))
