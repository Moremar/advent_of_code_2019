import numpy

BASE_PATTERN = [0, 1, 0, -1]
PATTERNS = []


def init_patterns(size):
    for i in range(1, size + 1):
        pattern = []
        while len(pattern) < size + 1:
            for j in range(len(BASE_PATTERN)):
                pattern += i * [BASE_PATTERN[j]]
        PATTERNS.append(pattern[1:size+1])


def next_phase(phase):
    return [abs(sum(numpy.multiply(phase, PATTERNS[i]))) % 10 for i in range(len(phase))]


def get_digits(phase):
    return "".join([str(i) for i in phase])[:8]


def solve(phase):
    init_patterns(len(phase))
    for i in range(100):
        phase = next_phase(phase)
    return get_digits(phase)


def parse(file_name):
    with open(file_name, "r") as f:
        return [int(c) for c in f.readline().strip()]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
