WIDTH = 25
HEIGHT = 6


def count_per_layer(layer, digit):
    return sum([line.count(str(digit)) for line in layer])


def solve(layers):
    min_zeroes = WIDTH * HEIGHT
    score = None
    for layer in layers:
        zeroes = count_per_layer(layer, 0)
        if min_zeroes > zeroes:
            min_zeroes = zeroes
            score = count_per_layer(layer, 1) * count_per_layer(layer, 2)
    return score


def parse(file_name):
    with open(file_name, "r") as f:
        layers = []
        line = f.readline().strip()
        while len(line) > 0:
            layer = []
            for i in range(0, HEIGHT):
                row = []
                for j in range(0, WIDTH):
                    row.append(line[j])
                layer.append(row)
                line = line[WIDTH:]
            layers.append(layer)
        return layers


if __name__ == '__main__':
    print(solve(parse("data.txt")))
