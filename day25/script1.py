from day21.script1 import parse, Program, to_codes, to_ascii
import re

DIRECTIONS = ["north", "east", "south", "west"]
DANGEROUS_ITEMS = ["infinite loop", "giant electromagnet", "escape pod", "photons", "molten lava"]


def get_combinations_rec(so_far, items, res):
    if len(items) == 0:
        res.append(so_far)
    else:
        get_combinations_rec(so_far, items[1:], res)
        get_combinations_rec(so_far + [items[0]], items[1:], res)


def get_combinations(items):
    res = []
    get_combinations_rec([], items, res)
    return res


def parse_room_output(ascii_output):
    room_name = None
    directions = []
    items = []
    for line in ascii_output.split("\n"):
        if len(line) == 0:
            continue
        if line[0:2] == "==":
            room_name = line.split("==")[1].strip()
        elif line[0] == "-":
            option = line[1:].strip()
            if option in DIRECTIONS:
                directions.append(option)
            else:
                items.append(option)
    return room_name, directions, items


def opposite(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) + 2) % len(DIRECTIONS)]


def simplify_path(path):
    # remove the successive opposite directions to avoid unnecessary instructions
    simple_path = list(path)
    i = 0
    while i < len(simple_path) - 1:
        if simple_path[i] == opposite(simple_path[i+1]):
            simple_path = simple_path[:i] + simple_path[i+2:]
            i = 0
        else:
            i += 1
    return simple_path


class Room:
    def __init__(self, room_id, name, directions):
        self.room_id = room_id
        self.name = name
        self.to_explore = directions
        self.explored = {}

    def __repr__(self):
        return "Room({}, {}, {}, {})".format(self.room_id, self.name, self.to_explore, self.explored)

    def explore(self, direction, room_name):
        if direction in self.explored:
            print("already explored ", direction, " from room ", self.name, ", skip.")
        elif direction not in self.to_explore:
            raise ValueError("Direction not available: ", direction)
        else:
            self.to_explore.remove(direction)
            self.explored[direction] = room_name


class State:
    def __init__(self, memory):
        self.pgm = Program(memory, [])
        self.curr_room = None
        self.rooms = {}
        self.items = []
        self.instructions = []  # useful for debug to track all instructions given to the pgm
        self.path_to_sensor = None
        self.paths_to_explore = []

    def run_instruction(self, instruction):
        # print("EXECUTING INSTRUCTION: ", instruction)
        self.instructions.append(instruction)
        self.pgm.inputs = to_codes(instruction + ("" if instruction == "" else "\n"))
        self.pgm.run()
        ascii_output = to_ascii(self.pgm.outputs)
        # print("OUTPUT : ", ascii_output)
        self.pgm.outputs = []
        return ascii_output

    def init(self):
        output = self.run_instruction("")
        (room_name, directions, _) = parse_room_output(output)
        self.pgm.outputs = []
        self.curr_room = Room(0, room_name, directions)
        self.rooms[room_name] = self.curr_room
        self.paths_to_explore = [[direction] for direction in directions]

    def update_paths(self, direction):
        """Keep the list of directions to follow to go to each unexplored path"""
        for path in self.paths_to_explore:
            path.insert(0, opposite(direction))
        if self.path_to_sensor is not None:
            self.path_to_sensor.insert(0, opposite(direction))

    def move(self, direction):
        output = self.run_instruction(direction)
        (room_name, directions, items) = parse_room_output(output)

        # update the world map with the new room
        self.update_paths(direction)
        if room_name in self.rooms:
            next_room = self.rooms[room_name]
        else:
            next_room = Room(len(self.rooms), room_name, directions)
            self.rooms[room_name] = next_room
            new_directions = [d for d in directions if d != opposite(direction)]
            if room_name == "Security Checkpoint":
                # Next room is the sensor, we want to explore all before to get all objects
                # print("SENSOR IS NEXT, GO BACK GET ALL OBJECTS !")
                self.path_to_sensor = [new_directions[0]]
            else:
                self.paths_to_explore = [[d] for d in new_directions] + self.paths_to_explore

        self.curr_room.explore(direction, next_room.name)
        next_room.explore(opposite(direction), self.curr_room.name)
        self.curr_room = next_room

        # pick all available items
        for item in items:
            if item not in self.items and item not in DANGEROUS_ITEMS:
                self.run_instruction("take " + item)
                self.items.append(item)

    def next_turn(self):
        # pick the next unexplored path and go there
        if len(self.paths_to_explore) > 0:
            path = self.paths_to_explore.pop(0)
            path = simplify_path(path)
            # Move quickly until the last room already explored of the path
            for direction in path:
                self.move(direction)
            return -1
        else:
            # if no unexplored path, it's time to go to the sensor
            return self.handle_sensor()

    def set_items_combination(self, combination):
        # drop all we have
        for item in self.items:
            self.run_instruction("drop " + item)
        self.items = []
        # take those we want
        for item in combination:
            self.run_instruction("take " + item)
            self.items.append(item)

    def handle_sensor(self):
        # Go back to the checkpoint before the sensor
        if self.path_to_sensor is None:
            raise ValueError("No more path to check and the sensor was not found.")
        for direction in self.path_to_sensor[:-1]:
            self.move(direction)
        direction_to_sensor = self.path_to_sensor[-1]

        # Prepare all combinations of objects to use
        self.items = sorted(self.items)
        combinations = get_combinations(self.items)

        # Try all combinations one by one until the sensor lets us in
        for combination in combinations:
            self.set_items_combination(combination)
            output = self.run_instruction(direction_to_sensor)
            if "Alert" not in output:
                # found the correct combination, the password is the only number in the output
                _, password, _ = re.split(r"([0-9]+)", output)
                return int(password)


def solve(memory):
    state = State(memory)
    state.init()

    password = -1
    while password < 0:
        password = state.next_turn()
    return password


if __name__ == '__main__':
    print(solve(parse("data.txt")))
