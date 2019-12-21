from day18.script1 import parse_matrix, read_char_matrix, alpha_lower, solve_world


# We could use the same logic as part 1 with a state made of a distance and 4 (x, y) pairs (one for each bot)
# This works with examples, but there are too many combinations for the real input so it runs for very long
#
# To get it quicker, we will resolve the 4 sub-mazes independently, assuming we have all keys from other 3 mazes.
# Then we sum the 4 results.
#
# There could be cases where this logic does not work (basically if the keys from other mazes that we assume we have
# cannot be obtained in the order we assumed, because they require the current bot to get keys in a different order)
#
# I did not have such problematic cases with my input file and this logic gave the correct result.


def solve(world):
    (world1, keys1, world2, keys2, world3, keys3, world4, keys4) = world
    return solve_world(world1, keys1) \
        + solve_world(world2, keys2) \
        + solve_world(world3, keys3) \
        + solve_world(world4, keys4)


def parse(file_name):
    matrix = read_char_matrix(file_name)
    middle_i = (len(matrix) + 1) // 2
    middle_j = (len(matrix[0]) + 1) // 2

    # split into 4 sub-matrices
    (mx1, mx2, mx3, mx4) = [], [], [], []
    (keys1, keys2, keys3, keys4) = [], [], [], []

    for i in range(middle_i):
        row = []
        for j in range(middle_j):
            row.append(matrix[i][j])
            if matrix[i][j] in alpha_lower:
                keys1.append(matrix[i][j])
        mx1.append(row)

    for i in range(middle_i):
        row = []
        for j in range(middle_j, len(matrix[0])):
            row.append(matrix[i][j])
            if matrix[i][j] in alpha_lower:
                keys2.append(matrix[i][j])
        mx2.append(row)

    for i in range(middle_i, len(matrix)):
        row = []
        for j in range(middle_j):
            row.append(matrix[i][j])
            if matrix[i][j] in alpha_lower:
                keys3.append(matrix[i][j])
        mx3.append(row)

    for i in range(middle_i, len(matrix)):
        row = []
        for j in range(middle_j, len(matrix[0])):
            row.append(matrix[i][j])
            if matrix[i][j] in alpha_lower:
                keys4.append(matrix[i][j])
        mx4.append(row)

    return parse_matrix(mx1), keys1, \
        parse_matrix(mx2), keys2, \
        parse_matrix(mx3), keys3, \
        parse_matrix(mx4), keys4


if __name__ == '__main__':
    print(solve(parse("data2.txt")))
