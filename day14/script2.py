from day14.script1 import parse, Reaction, produce_fuel

# There is too much ore, so generating the fuel 1 by 1 takes too long
# Instead we will generate the fuels X by X
# First we take a big X and generate as many times X fuels as we can
# Then we take a smaller X and generate fuels X by X with the remaining ores
# Then we use the original reaction to generate the last fuels 1 by 1


def solve(reactions):

    ores = 1000000000000
    fuels = 0
    reserve = {}

    # calibrated a bit arbitrary to get it to execute in ~5 sec
    X1 = 100000
    X2 = 1000

    # Multiply the FUEL reaction by X to generate fuel X by X
    reac = [r for r in reactions if r.chemical_out[0] == "FUEL"][0]
    reacX1 = Reaction([(e[0], e[1] * X1) for e in reac.chemical_in], ("FUEL", X1))
    reacX2 = Reaction([(e[0], e[1] * X2) for e in reac.chemical_in], ("FUEL", X2))
    reactions.remove(reac)
    reactions.append(reacX1)

    # Generate fuel X1 by X1
    cost = produce_fuel(reactions, reserve)
    while cost <= ores:
        ores -= cost
        fuels += X1
        cost = produce_fuel(reactions, reserve)

    # No longer possible to generate X1 fuels, switch to X2
    reactions.remove(reacX1)
    reactions.append(reacX2)

    # Generate fuel X2 by X2
    cost = produce_fuel(reactions, reserve)
    while cost <= ores:
        ores -= cost
        fuels += X2
        cost = produce_fuel(reactions, reserve)

    # No longer possible to generate X2 fuels, switch to the original reaction
    reactions.remove(reacX2)
    reactions.append(reac)

    # Generate fuel 1 by 1
    cost = produce_fuel(reactions, reserve)
    while cost <= ores:
        ores -= cost
        fuels += 1
        cost = produce_fuel(reactions, reserve)

    return fuels


if __name__ == '__main__':
    print(solve(parse("data.txt")))
