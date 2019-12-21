from day18.script1 import read_char_matrix

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Cell:
    def __init__(self, i, j, value):
        self.i = i
        self.j = j
        self.value = value
        self.adjacent = []

    def is_portal(self):
        return len(self.value) == 2 and self.value not in ["AA", "ZZ"]

    def __repr__(self):
        return "Cell({0}, {1}, {2}, {3})".format(self.i, self.j, self.value, self.adjacent)


class State:
    def __init__(self, distance, visited):
        self.distance = distance
        self.visited = visited

    def copy(self):
        return State(self.distance, list(self.visited))


def has_a_chance(i, j, distance, state_map, end):
    # skip if we already found a shorter route to the end
    if end in state_map and distance >= state_map[end]:
        return False

    # skip if we already found a shorter route to this specific cell
    if (i, j) in state_map and state_map[(i, j)] <= distance:
        return False

    return True


def solve(world):
    (graph, start, end, outer_portals, inner_portals) = world
    state_map = {}
    to_check = [State(0, [start])]
    while len(to_check) > 0:
        state = to_check.pop(0)
        cell = graph[state.visited[-1]]

        if not has_a_chance(cell.i, cell.j, state.distance, state_map, end):
            continue

        # record the distance to the current cell
        state_map[(cell.i, cell.j)] = state.distance

        # add the adjacent nodes to be processed
        for (x, y, d) in cell.adjacent:
            next_state = state.copy()
            next_state.distance += d
            next_state.visited.append((x, y))
            to_check.append(next_state)

        # if it is a portal, add the route through the portal
        if cell.is_portal():
            portal_dest = inner_portals if (cell.i, cell.j) in outer_portals.values() else outer_portals
            next_state = state.copy()
            next_state.distance += 1
            next_state.visited.append(portal_dest[cell.value])
            to_check.append(next_state)

    return state_map[end]


def parse(file_name):
    graph = {}
    inner_portals = {}
    outer_portals = {}
    matrix = read_char_matrix(file_name)

    # Go through the matrix of chars and build the graph
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            c = matrix[i][j]
            if c in ["#", " "]:
                continue
            elif c == ".":
                graph[(i, j)] = Cell(i, j, c)
                # connect to the cells above and before if needed
                for (x, y) in [(i - 1, j), (i, j - 1)]:
                    if (x, y) in graph:
                        graph[(x, y)].adjacent.append((i, j, 1))
                        graph[(i, j)].adjacent.append((x, y, 1))
                continue
            else:
                # A letter was found, need to locate the next one (on right or below)
                letter_below = (i != len(matrix) - 1 and matrix[i + 1][j] in ALPHABET)
                letter_right = (j != len(matrix[0]) - 1 and matrix[i][j + 1] in ALPHABET)
                if letter_below:
                    key = matrix[i][j] + matrix[i + 1][j]
                    cell = [(x, y) for (x, y) in [(i - 1, j), (i + 2, j)]
                            if 0 <= x < len(matrix) and matrix[x][y] == "."][0]
                    portals = outer_portals if (i == 0 or i == len(matrix) - 2) else inner_portals
                    portals[key] = cell
                elif letter_right:
                    key = matrix[i][j] + matrix[i][j + 1]
                    cell = [(x, y) for (x, y) in [(i, j - 1), (i, j + 2)]
                            if 0 <= y < len(matrix[0]) and matrix[x][y] == "."][0]
                    portals = outer_portals if (j == 0 or j == len(matrix[0]) - 2) else inner_portals
                    portals[key] = cell
                else:
                    continue  # 2nd char of an already processed portal

    # flag the portals
    for (key, portal) in outer_portals.items():
        graph[portal].value = key
    for (key, portal) in inner_portals.items():
        graph[portal].value = key

    # get the start and end of the maze
    start = outer_portals["AA"]
    del outer_portals["AA"]
    end = outer_portals["ZZ"]
    del outer_portals["ZZ"]

    for i in range(1, len(matrix)):  # no need to check the edge, they are walls
        for j in range(1, len(matrix[0])):
            if (i, j) in graph and graph[(i, j)].value == ".":
                # if it is a dead end, we remove it
                if len(graph[(i, j)].adjacent) == 1:
                    (i1, j1, d1) = graph[(i, j)].adjacent.pop()
                    graph[(i1, j1)].adjacent.remove((i, j, d1))
                else:
                    for (i1, j1, d1) in graph[(i, j)].adjacent:
                        for (i2, j2, d2) in graph[(i, j)].adjacent:
                            if (i1, j1) != (i2, j2):
                                if (i, j, d1) in graph[(i1, j1)].adjacent:
                                    # can be already removed for intersections
                                    graph[(i1, j1)].adjacent.remove((i, j, d1))

                                # Link i1 and i2 if they are not linked yet
                                if (i2, j2) not in [(x, y) for (x, y, _) in graph[(i1, j1)].adjacent]:
                                    graph[(i1, j1)].adjacent.append((i2, j2, d1 + d2))
                del graph[(i, j)]
    return graph, start, end, outer_portals, inner_portals


if __name__ == '__main__':
    print(solve(parse("data.txt")))
