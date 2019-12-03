from day03.script1 import parse
import sys


def contains(seg, x, y):
    """True if point (x,y) is on this segment"""
    return (seg.direction == "H" and seg.yA == y and seg.xA <= x <= seg.xB) \
           or (seg.direction == "V" and seg.xA == x and seg.yA <= y <= seg.yB)


def dist_to(wire, x, y):
    """Distance of a point from the origin along the wire"""
    dist = 0
    prev_seg = None
    for seg in wire:
        if contains(seg, x, y):
            # need to find which part of the segment to add
            # since A and B are not in occurring order but in coordinate orders,
            # we need a trick to find which of A or B is the first in occurring order
            last_edge = (0, 0)
            if prev_seg is not None:
                last_seg_A = (prev_seg.xA, prev_seg.yA)
                last_seg_B = (prev_seg.xB, prev_seg.yB)
                last_edge = last_seg_A if contains(seg, last_seg_A[0], last_seg_A[1]) else last_seg_B
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


if __name__ == '__main__':
    print(solve(parse("data.txt")))
