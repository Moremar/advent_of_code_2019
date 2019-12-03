import sys


class Segment:
    """A segment is either vertical or horizontal"""
    def __init__(self, xA, yA, xB, yB):
        # flip A and B if needed to always have A smaller than B
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

    def contains(self, x, y):
        """True if point (x,y) is on this segment"""
        return (self.direction == "H" and self.yA == y and self.xA <= x <= self.xB) \
               or (self.direction == "V" and self.xA == x and self.yA <= y <= self.yB)


def dist_to(wire, x, y):
    """Distance of a point from the origin along the wire"""
    dist = 0
    prev_seg = None
    for seg in wire:
        if seg.contains(x, y):
            # need to find which part of the segment to add
            # since A and B are not in occurring order but in coordinate orders,
            # we need a trick to find which of A or B is the first in occurring order
            last_edge = (0, 0)
            if prev_seg is not None:
                last_seg_A = (prev_seg.xA, prev_seg.yA)
                last_seg_B = (prev_seg.xB, prev_seg.yB)
                last_edge = last_seg_A if seg.contains(last_seg_A[0], last_seg_A[1]) else last_seg_B
            dist += abs(last_edge[0] - x) + abs(last_edge[1] - y)  # segment length
            return dist
        else:
            dist += (seg.xB - seg.xA) + (seg.yB - seg.yA)  # segment length
            prev_seg = seg
    raise ValueError("Intersection not found on the wire !")


def solve(wires):
    # for each segment of the second wire, check if it intersects the segments of the 1st wire
    intersects = []
    for seg1 in wires[1]:
        for seg2 in wires[0]:
            intersect = seg1.intersect(seg2)
            if intersect:
                intersects.append(intersect)

    # get the shortest distance along the wires to an intersection
    intersects.remove((0, 0))
    distance_min = sys.maxsize
    for intersect in intersects:
        dist1 = dist_to(wires[0], intersect[0], intersect[1])
        dist2 = dist_to(wires[1], intersect[0], intersect[1])
        if dist1 + dist2 < distance_min:
            distance_min = dist1 + dist2
    return distance_min


def parse(file_name):
    """Parse the data file"""
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
