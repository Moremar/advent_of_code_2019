from day20.script1 import parse


# We need to add the level in the state
class State:
    def __init__(self, distance, visited, level):
        self.distance = distance
        self.visited = visited
        self.level = level

    def __repr__(self):
        return "State({0}, {1}, {2})".format(self.distance, self.visited, self.level)

    def copy(self):
        return State(self.distance, list(self.visited), self.level)


def has_a_chance(i, j, level, distance, state_map, start, end):
    if (i, j) in [start, end] and level != 0:
        return False
    # skip if we already found a shorter route to the end
    if (end[0], end[1], 0) in state_map and distance >= state_map[(end[0], end[1], 0)]:
        return False
    # skip if we already found a shorter route to this specific cell
    if (i, j, level) in state_map and state_map[(i, j, level)] <= distance:
        return False
    return True


def solve(world):
    (graph, start, end, outer_portals, inner_portals) = world
    state_map = {}
    to_check = [State(0, [start], 0)]
    while len(to_check) > 0:
        state = to_check.pop(0)
        cell = graph[state.visited[-1]]

        if not has_a_chance(cell.i, cell.j, state.level, state.distance, state_map, start, end):
            continue

        # record the distance to the current cell
        state_map[(cell.i, cell.j, state.level)] = state.distance

        # add the adjacent nodes on the same level to be processed
        for (x, y, d) in cell.adjacent:
            next_state = state.copy()
            next_state.distance += d
            next_state.visited.append((x, y))
            if has_a_chance(x, y, next_state.level, next_state.distance, state_map, start, end):
                to_check.append(next_state)

        if cell.is_portal():
            if (cell.i, cell.j) in outer_portals.values():
                # if it is an outer portal, go down one level
                if state.level == 0:
                    continue  # cannot go lower than level 0, portal is regarded as a wall
                next_state = state.copy()
                next_state.distance += 1
                next_state.level -= 1
                dest = inner_portals[cell.value]
                next_state.visited.append(dest)
                if has_a_chance(dest[0], dest[1], next_state.level, next_state.distance, state_map, start, end):
                    to_check.append(next_state)
            else:
                # if it is an inner portal, go up one level
                next_state = state.copy()
                next_state.distance += 1
                next_state.level += 1
                dest = outer_portals[cell.value]
                next_state.visited.append(dest)
                if has_a_chance(dest[0], dest[1], next_state.level, next_state.distance, state_map, start, end):
                    to_check.append(next_state)

    return state_map[end[0], end[1], 0]


if __name__ == '__main__':
    print(solve(parse("data.txt")))
