alpha_lower = "abcdefghijklmnopqrstuvwxyz"
alpha_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Cell:
    def __init__(self, i, j, value):
        self.i = i
        self.j = j
        self.value = value
        self.adjacent = []

    def get_type(self):
        if self.value == "@":
            return "START"
        elif self.value == ".":
            return "EMPTY"
        elif self.value == "+":
            return "CROSS"
        elif self.value in alpha_lower:
            return "KEY"
        elif self.value in alpha_upper:
            return "DOOR"
        else:
            raise ValueError("Invalid type: ", self.value)

    def get_key(self):
        if self.get_type() != "DOOR":
            raise ValueError("Only DOOR places have a key")
        return alpha_lower[alpha_upper.index(self.value)]

    def __repr__(self):
        return "Cell({0}, {1}, {2}, {3}, {4})".format(self.i, self.j, self.value, self.get_type(), self.adjacent)


class State:
    def __init__(self, keys, distance, visited):
        self.keys = keys
        self.distance = distance
        self.visited = visited

    def get_keys_str(self):
        return "".join(sorted(self.keys))

    def copy(self):
        return State(list(self.keys), self.distance, list(self.visited))


def solve_world(world, valid_keys=alpha_lower):
    graph, starts, key_count = world
    start = starts[0]  # only 1 start in part 1
    best_dist = -1
    state_map = {start: {"": 0}}
    states = [State([], 0, [start])]

    while len(states) > 0:
        state = states.pop(0)

        # stop if a shorter result path is already found
        if -1 < best_dist <= state.distance:
            continue

        cell = graph[state.visited[-1]]
        for (x, y, d) in cell.adjacent:
            adj_cell = graph[(x, y)]

            # useless to go to a door we cant open
            if adj_cell.get_type() == "DOOR" \
                    and adj_cell.get_key() not in state.keys \
                    and adj_cell.get_key() in valid_keys:
                continue

            # useless to go back if we did not just get a new key
            if len(state.visited) >= 2 and (x, y) == state.visited[-2] and cell.get_type() != "KEY":
                continue

            next_state = state.copy()
            next_state.distance += d
            next_state.visited.append((x, y))
            if adj_cell.get_type() == "KEY" and adj_cell.value not in next_state.keys:
                next_state.keys.append(adj_cell.value)
                if len(next_state.keys) == key_count:
                    if best_dist == -1 or next_state.distance < best_dist:
                        best_dist = next_state.distance

            # Add it to the states list if relevant
            if (x, y) not in state_map:
                state_map[(x, y)] = {}
            key_str = next_state.get_keys_str()
            if key_str not in state_map[(x, y)] or state_map[(x, y)][key_str] > next_state.distance:
                # we have never been yet to this cell with this set of keys in a smaller distance
                state_map[(x, y)][key_str] = next_state.distance
                states.append(next_state)
    return best_dist


def solve(world):
    return solve_world(world)


def read_char_matrix(file_name):
    with open(file_name, "r") as f:
        # create a matrix of chars
        matrix = []
        for line in [line.strip("\n") for line in f.readlines()]:
            row = []
            for c in line:
                row.append(c)
            matrix.append(row)
    return matrix


def parse_matrix(matrix):
    # build graph with one edge per cell
    graph = {}
    starts = []
    key_count = 0

    # Go through the matrix of chars and build the graph
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            c = matrix[i][j]
            if c != "#":
                graph[(i, j)] = Cell(i, j, c)
                if graph[(i, j)].get_type() == "START":
                    starts.append((i, j))
                elif graph[(i, j)].get_type() == "KEY":
                    key_count += 1
                # connect to the cells above and before if needed
                for (x, y) in [(i-1, j), (i, j-1)]:
                    if (x, y) in graph:
                        graph[(x, y)].adjacent.append((i, j, 1))
                        graph[(i, j)].adjacent.append((x, y, 1))

    for i in range(1, len(matrix)):      # no need to check the edge, they are walls
        for j in range(1, len(matrix[0])):
            if (i, j) in graph and graph[(i, j)].get_type() == "EMPTY":

                # if it is a dead end, we remove it
                if len(graph[(i, j)].adjacent) == 1:
                    (i1, j1, d1) = graph[(i, j)].adjacent.pop()
                    graph[(i1, j1)].adjacent.remove((i, j, d1))

                else:
                    for (i1, j1, d1) in graph[(i, j)].adjacent:
                        for (i2, j2, d2) in graph[(i, j)].adjacent:
                            if (i1, j1) == (i2, j2):
                                continue

                            if (i, j, d1) in graph[(i1, j1)].adjacent:  # can be already removed for intersections
                                graph[(i1, j1)].adjacent.remove((i, j, d1))

                            # Link i1 and i2 if they are not linked yet
                            links = [(x, y, d) for (x, y, d) in graph[(i1, j1)].adjacent if x == i2 and y == j2]
                            if len(links) == 0:
                                graph[(i1, j1)].adjacent.append((i2, j2, d1 + d2))
                            else:
                                link = links[0]
                                if link[2] > d1 + d2:
                                    graph[(i1, j1)].adjacent.remove((i2, j2, link[2]))
                                    graph[(i1, j1)].adjacent.append((i2, j2, d1 + d2))
                del graph[(i, j)]
    return graph, starts, key_count


def parse(file_name):
    matrix = read_char_matrix(file_name)
    return parse_matrix(matrix)


if __name__ == '__main__':
    print(solve(parse("data.txt")))
