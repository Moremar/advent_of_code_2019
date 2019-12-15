from day15.script1 import parse, visit_area, WALL, EMPTY, OXYGEN


def get_bounds(visited):
    return (min([x for (x, _) in visited]), max([x for (x, _) in visited]),
            min([y for (_, y) in visited]), max([y for (_, y) in visited]))


def get_area_map(visited):
    area = ""
    (x_min, x_max, y_min, y_max) = get_bounds(visited)
    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1):
            if (x, y) in visited:
                area += "#" if visited[(x, y)] == WALL else "O" if visited[(x, y)] == OXYGEN else "."
            else:
                area += " "
        area += "\n"
    return area


def has_oxygen_around(pos, visited):
    for next_pos in [(pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)]:
        if next_pos in visited and visited[next_pos] == OXYGEN:
            return True
    return False


def solve(pgm):
    (_, visited) = visit_area(pgm, False)
    area = get_area_map(visited)
    print("Area map:\n", area)
    elapsed = 0
    while "." in area:
        elapsed += 1
        to_oxygenize = []
        for pos in visited:
            if visited[pos] == EMPTY and has_oxygen_around(pos, visited):
                to_oxygenize.append(pos)
        for pos in to_oxygenize:
            visited[pos] = OXYGEN
        area = get_area_map(visited)

    return elapsed


if __name__ == '__main__':
    print(solve(parse("data.txt")))
