import re
import copy
import numpy as np
import itertools

MOON_PARSER = re.compile(r"\<x=(?P<x>[-]?\d+), y=(?P<y>[-]?\d+), z=(?P<z>[-]?\d+)\>")

def velocity(m1, m2):
    v = [0, 0, 0]
    for i in range(3):
        m1v = m1.position[i]
        m2v = m2.position[i]

        if m1v > m2v:
            v[i] = -1
        elif m1v == m2v:
            continue
        elif m1v < m2v:
            v[i] = +1
    return v

class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def __str__(self):
        pos = f"pos=<x={self.position[0]}, y={self.position[1]}, z={self.position[2]}>"
        vel = f"vel=<x={self.velocity[0]}, y={self.velocity[1]}, z={self.velocity[2]}>"
        return f"{pos}, {vel}"

    def calculate_velocity(self, moons):
        moons = filter(lambda x: x != self, moons)
        new_velocity = [0, 0, 0]
        for m in moons:
            v = velocity(self, m)
            new_velocity[0] += v[0]
            new_velocity[1] += v[1]
            new_velocity[2] += v[2]

        self.velocity[0] += new_velocity[0]
        self.velocity[1] += new_velocity[1]
        self.velocity[2] += new_velocity[2]
        return self.velocity

    def apply(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]

    def pot(self):
        return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])

    def kin(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])

    def energy(self):
        return self.pot() * self.kin()


def step(moons):
    for m in moons:
        m.calculate_velocity(moons)

    for m in moons:
        m.apply()
        # print(m)

def simulate_moons(moons, interations):
    for i in range(interations + 1):
        print(f"=== {i} ===")
        if i == 0:
            for m in moons:
                print(m)
        else:
            step(moons)
    energy = sum([m.energy() for m in moons])
    return energy

def state(moons, d):
    return [m.position[d] for m in moons] + [m.velocity[d] for m in moons]

def simulate_moons_2(moons):
    i = 0
    initial_state = [
        state(moons, x) for x in range(3)
    ]
    cycle_len = [0, 0, 0]
    while (
        cycle_len[0] == 0 or cycle_len[1] == 0 or cycle_len[2] == 0
    ):
        step(moons)
        i += 1

        if i % 100 == 0:
            print(i, cycle_len)

        for d in range(3):
            if cycle_len[d] == 0 and state(moons, d) == initial_state[d]:
                cycle_len[d] = i
                print(cycle_len)

    print(cycle_len)
    result = np.lcm(cycle_len[0], np.lcm(cycle_len[1], cycle_len[2]))
    return result

def create_moon(input):
    m = MOON_PARSER.match(input)
    position = [int(m["x"], 10), int(m["y"], 10), int(m["z"], 10)]
    return Moon(position)

def parse_input(input):
    moons = []
    for l in input.split("\n"):
        moons.append(create_moon(l))
    return moons


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    moons = parse_input(data)

    print(simulate_moons(moons, 1000))

def main2():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    moons = parse_input(data)

    print(simulate_moons_2(moons))


if __name__ == "__main__":
    main2()