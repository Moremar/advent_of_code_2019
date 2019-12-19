from day19.script1 import parse, is_in_beam

SHIP_SIZE = 100
START_Y = 100


def solve(memory):
    beam = {}

    # initialize the beam
    x1 = 0
    while not is_in_beam(memory, x1, START_Y):
        x1 += 1
    x2 = x1
    while is_in_beam(memory, x2, START_Y):
        x2 += 1
    beam[START_Y] = [x1, x2-1]

    # find the first and last X of the beam for each line until it fits
    y = START_Y + 1
    while True:
        x1 = beam[y-1][0]
        while not is_in_beam(memory, x1, y):
            x1 += 1
        x2 = beam[y-1][1] + 1
        while is_in_beam(memory, x2, y):
            x2 += 1
        beam[y] = [x1, x2-1]

        if y > START_Y + SHIP_SIZE:
            y0 = y - (SHIP_SIZE - 1)
            i0 = beam[y0][1] - (SHIP_SIZE - 1)
            if i0 >= beam[y0][0]:  # the beam is at least SHIP_SIZE wide
                if x1 <= i0:
                    return (i0 * 10000) + y0
        y += 1


if __name__ == '__main__':
    print(solve(parse("data.txt")))
