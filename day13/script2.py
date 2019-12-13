import os

graphic = False
if "PYCHARM" in os.environ:
    # if running from Pycharm, we cannot clear the terminal to make a smooth animation
    # (PYCHARM env var set in the Debug configuration)
    from day13 import program
else:
    # if running from day13/ folder in a terminal (to see the animation)
    graphic = True
    import time
    import program


EMPTY, WALL, BLOCK, PADDLE, BALL, SCORE = 0, 1, 2, 3, 4, 5
LEFT, CENTER, RIGHT = -1, 0, 1


def get_char(state, i, j):
    obj = state[i][j]
    return "#" if obj == WALL else "@" if obj == BLOCK else "_" if obj == PADDLE else "o" if obj == BALL else " "


def draw(state, max_i, max_j):
    for j in range(0, max_j + 1):
        string = ""
        for i in range(0, max_i + 1):
            string += get_char(state, i, j)
        print(string)


def update_state(out, state, score):
    ball = (-1, -1)
    paddle = (-1, -1)
    while len(out) > 0:
        (i, j, k) = (out.pop(0), out.pop(0), out.pop(0))
        if (i, j) == (-1, 0):
            score = k
        else:
            if k == PADDLE:
                paddle = (i, j)
            elif k == BALL:
                ball = (i, j)
            state[i][j] = k
    return score, ball, paddle


def decide_next_move(ball, paddle):
    # Always move the paddle in direction of the ball
    if ball[0] - paddle[0] > 0:
        return RIGHT
    elif ball[0] - paddle[0] < 0:
        return LEFT
    else:
        return CENTER


def solve(pgm):
    # Run the program with no input to get the initial state
    pgm.memory[0] = 2
    pgm.run()
    state, score = [], 0
    out = pgm.outputs
    sequences = [(out[i], out[i+1], out[i+2]) for i in range(len(out)) if i % 3 == 0]
    max_i = max([i for (i, j, k) in sequences])
    max_j = max([j for (i, j, k) in sequences])

    # Build the grid
    for i in range(0, max_i + 2):
        state.append([0] * (max_j + 2))
    (score, ball, paddle) = update_state(pgm.outputs, state, score)
    draw(state, max_i, max_j)

    while not pgm.completed:
        pgm.inputs.append(decide_next_move(ball, paddle))
        pgm.run()
        (score, ball, paddle) = update_state(pgm.outputs, state, score)

        if graphic:
            # Print nicely to see the animated game
            os.system('clear')
            draw(state, max_i, max_j)
            time.sleep(0.05)

    return score


def parse(file_name):
    with open(file_name, "r") as f:
        memory = [int(x) for x in f.readline().strip().split(",")]
        return program.Program(memory, [])


if __name__ == '__main__':
    print(solve(parse("data.txt")))
