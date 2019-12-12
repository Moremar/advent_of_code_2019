from day12.script1 import parse, step
from math import gcd


def v_coords(moons):
    return [moon.vx for moon in moons], [moon.vy for moon in moons], [moon.vz for moon in moons]


def solve(moons):
    # The velocity is equal to 0 at every half period.
    # vx, vy and vz coords behave totally independently
    # instead of finding a period for (vx, vy, vz), we find the period for vx, vy and vz separately
    # then the period of (vx, vy, vz) is the smallest multiple of these 3 periods
    # Then multiply by 2 to get the period of the system (where x, y, z are the same as initially)

    vx_init, vy_init, vz_init = v_coords(moons)
    turn = 0
    v_periods = [0, 0, 0]
    while True:
        turn += 1
        moons = step(moons)
        vx, vy, vz = v_coords(moons)
        if vx == vx_init and v_periods[0] == 0:
            v_periods[0] = turn
        if vy == vy_init and v_periods[1] == 0:
            v_periods[1] = turn
        if vz == vz_init and v_periods[2] == 0:
            v_periods[2] = turn
        if 0 not in v_periods:
            return smallest_multiple(v_periods) * 2  #


def smallest_multiple(numbers):
    lcm = numbers[0]
    for number in numbers[1:]:
        lcm = int(lcm * number / gcd(lcm, number))

    return lcm


if __name__ == '__main__':
    print(solve(parse("data.txt")))
