from day13.script1 import Program

WALL, EMPTY, OXYGEN = (0, 1, 2)


class Cell:
    def __init__(self, pos, inputs, distance):
        self.pos = pos            # coordinates
        self.inputs = inputs      # inputs to get there from (0, 0)
        self.distance = distance  # how far from (0, 0)

    def way_back(self):
        # how to go back to (0, 0)
        back = reversed(list(self.inputs))
        return [(1 if a == 2 else 2 if a == 1 else 3 if a == 4 else 4) for a in back]

    def next_cells(self):
        return [
            Cell((self.pos[0], self.pos[1] + 1), self.inputs + [1], self.distance + 1),
            Cell((self.pos[0], self.pos[1] - 1), self.inputs + [2], self.distance + 1),
            Cell((self.pos[0] - 1, self.pos[1]), self.inputs + [3], self.distance + 1),
            Cell((self.pos[0] + 1, self.pos[1]), self.inputs + [4], self.distance + 1)
        ]


def visit_area(pgm, stop_on_oxygen):
    visited = {(0, 0): EMPTY}
    oxygen_distance = 0
    to_visit = [Cell((0, 1), [1], 1), Cell((0, -1), [2], 1),
                Cell((-1, 0), [3], 1), Cell((1, 0), [4], 1)]
    while len(to_visit) > 0:
        # go to an unvisited cell with minimum distance from (0, 0)
        cell = to_visit.pop(0)
        pgm.inputs = list(cell.inputs)
        pgm.run()
        output = pgm.outputs[-1]  # last output is the result for the unvisited cell
        pgm.outputs = []
        if output == WALL:
            visited[cell.pos] = WALL
            cell.inputs.pop(len(cell.inputs)-1)  # drop the last command since no move
        elif output in [EMPTY, OXYGEN]:
            # add its unvisited neighbours
            visited[cell.pos] = output
            for next_cell in cell.next_cells():
                if next_cell.pos not in visited:
                    to_visit.append(next_cell)
        if output == OXYGEN:
            oxygen_distance = cell.distance
            if stop_on_oxygen:
                break
        # go back to (0, 0) for next cell exploration
        pgm.inputs = list(cell.way_back())
        pgm.run()
        pgm.outputs = []
    return oxygen_distance, visited


def solve(pgm):
    (oxygen_distance, _) = visit_area(pgm, True)
    return oxygen_distance


def parse(file_name):
    with open(file_name, "r") as f:
        memory = [int(x) for x in f.readline().strip().split(",")]
        return Program(memory, [])


if __name__ == '__main__':
    print(solve(parse("data.txt")))
