from day08.script1 import parse, WIDTH, HEIGHT


def solve(layers):
    image = []

    # start with all pixels transparent
    for i in range(0, HEIGHT):
        image.append(['2'] * WIDTH)

    # each layer will print on transparent pixels
    for layer in layers:
        for i in range(0, HEIGHT):
            for j in range(0, WIDTH):
                if image[i][j] == '2':
                    image[i][j] = layer[i][j]

    # build the image in a readable way
    image_str = ""
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if image[i][j] == "0":
                image_str += " "
            elif image[i][j] == "1":
                image_str += "@"
            else:
                raise ValueError("Unexpected color: ", image[i][j])
        image_str += "\n"
    return image_str


if __name__ == '__main__':
    print(solve(parse("data.txt")))
