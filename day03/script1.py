class Segment:
    """Segments are either vertical or horizontal"""
    def __init__(self, xA, yA, xB, yB):
        # flip A and B if needed to always have A smaller than B, it saves a bunch of ifs later
        if xA > xB or yA > yB:
            (xA, yA, xB, yB) = (xB, yB, xA, yA)
        (self.xA, self.yA, self.xB, self.yB) = (xA, yA, xB, yB)
        self.direction = "H" if yA == yB else "V"

    def __repr__(self):
        """String representation for better readability in debugger"""
        return "Seg({0}, {1}, {2}, {3})".format(self.xA, self.yA, self.xB, self.yA, self.direction)

    def intersect(self, seg):
        """Find the intersection point of 2 segments if any"""
        if self.direction != seg.direction:
            seg_h = self if self.direction == "H" else seg
            seg_v = self if self.direction == "V" else seg
            if seg_v.yA <= seg_h.yA <= seg_v.yB and seg_h.xA <= seg_v.xA <= seg_h.xB:
                return (seg_v.xA, seg_h.yA)
            else:
                return None
        elif self.direction == "H":  # both segments horizontal
            if self.yA != seg.yA:
                return None
            if self.xA <= seg.xA <= self.xB or seg.xA <= self.xA <= seg.xB:  # segments overlap
                return (max(self.xA, seg.xA), self.yA)
        else:                        # both segments vertical
            if self.xA != seg.xA:
                return None
            if self.yA <= seg.yA <= self.yB or seg.yA <= self.yA <= seg.yB:  # segments overlap
                return (self.xA, max(self.yA, seg.yA))


def solve(wires):
    # get all intersection points of the 2 wires
    intersects = []
    for seg1 in wires[1]:
        for seg2 in wires[0]:
            intersect = seg1.intersect(seg2)
            if intersect:
                intersects.append(intersect)

    # get the distance of the intersection point closest from the center
    intersects.remove((0, 0))
    if len(intersects) == 0:
        raise ValueError("No intersection found.")
    distance_min = abs(intersects[0][0]) + abs(intersects[0][1])
    for (x, y) in intersects:
        distance = abs(x) + abs(y)
        if distance < distance_min:
            distance_min = distance
    return distance_min


def parse(file_name):
    """Parse the data file into the list of segments for each wire"""
    with open(file_name, "r") as f:
        wires = []
        for line in f.readlines():
            wire = []
            directions = line.split(",")
            (xA, yA) = (0, 0)
            for direction in directions:
                (xB, yB) = (xA, yA)
                shift = int(direction[1:])
                if direction[0] == "R":
                    xB += shift
                elif direction[0] == "L":
                    xB -= shift
                elif direction[0] == "U":
                    yB += shift
                elif direction[0] == "D":
                    yB -= shift
                else:
                    raise ValueError("Undefined direction: ", direction[0])
                wire.append(Segment(xA, yA, xB, yB))
                (xA, yA) = (xB, yB)
            wires.append(wire)
        return wires


if __name__ == '__main__':
    print(solve(parse("data.txt")))
