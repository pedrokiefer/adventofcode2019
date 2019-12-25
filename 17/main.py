from intcode import IntComputer
from difflib import SequenceMatcher

UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"

TURN_RIGHT = "R"
TURN_LEFT = "L"


DIRECTIONS = {
    UP: (0, -1),
    DOWN: (0, 1),
    RIGHT: (1, 0),
    LEFT: (-1, 0),
}

VALID_TURNS = {
    UP: ((DIRECTIONS[LEFT], LEFT), (DIRECTIONS[RIGHT], RIGHT)),
    RIGHT: ((DIRECTIONS[UP], UP), (DIRECTIONS[DOWN], DOWN)),
    DOWN: ((DIRECTIONS[RIGHT], RIGHT), (DIRECTIONS[LEFT], LEFT)),
    LEFT: ((DIRECTIONS[DOWN], DOWN), (DIRECTIONS[UP], UP)),
}

TURNS = [TURN_LEFT, TURN_RIGHT]

def find_bounds(m):
    keys = list(m.keys())

    xmin = min(keys)[0]
    xmax = max(keys)[0]

    ymin = min(keys)[1]
    ymax = max(keys)[1]

    return xmin, xmax, ymin, ymax


def str_to_map(input):
    input = input.strip()
    x = 0
    y = 0
    m = {}
    for l in input.split("\n"):
        x = 0
        for c in l:
            m[(x, y)] = c
            x += 1
        y += 1
    return m


def print_map(m):
    xmin, xmax, ymin, ymax = find_bounds(m)

    lines = []
    for y in range(ymin, ymax + 1):
        l = ""
        for x in range(xmin, xmax + 1):
            v = m.get((x, y), None)
            if v:
                l += v
        lines.append(l)

    return "\n".join(lines)


def point_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def search_all_directions(map, point):
    for d in DIRECTIONS.values():
        p = point_add(point, d)
        nv = map.get(p, None)
        if nv != "#":
            return False
    return True


def find_intersections(map):
    xmin, xmax, ymin, ymax = find_bounds(map)

    intersections = []

    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            v = map.get((x, y), None)
            if not v or v != "#":
                continue

            if search_all_directions(map, (x, y)):
                intersections.append((x, y))

    return intersections

def calibrate(intersections):
    return sum([ x * y for x, y in intersections ])


def find_vaccumm_robots(m):
    robots = []
    for k, v in m.items():
        if v in "^v<>":
            robots.append((k, v))
    return robots

def can_keep_bearing_for(robot, m):
    c = 0
    p = robot[0]
    next_p = point_add(p, DIRECTIONS[robot[1]])
    while True:
        v = m.get(next_p, None)
        if v == "#":
            p = next_p
            next_p = point_add(p, DIRECTIONS[robot[1]])
            c += 1
        else:
            break
    return (p, robot[1]), c

def can_turn(robot, m):
    print(robot)
    valid_turns = VALID_TURNS[robot[1]]
    for i, t in enumerate(valid_turns):
        p = point_add(robot[0], t[0])
        v = m.get(p, None)
        if v == "#":
            return (robot[0], t[1]), TURNS[i]
    print(f"=== Invalid turn: {robot}")
    return None, None


def find_path(robot, m):
    path = []

    while True:
        robot_n, c = can_keep_bearing_for(robot, m)
        if c > 0:
            robot = robot_n
            path.append(str(c))
        robot, t = can_turn(robot, m)
        if t:
            path.append(t)
        else:
            break
    return path

def all_sequences_of(path):
    sequences = []
    path_length = len(path)

    for window in range(20, 1, -1):
        j = 0
        while True:
            print(path_length - window, j)
            if path_length - window <= j:
                break
            seq1 = path[j:j+window]
            print(seq1)

            if len(",".join(seq1)) > 20:
                j += 1
                continue

            sequences.append(seq1)
            j += 1
    print(sequences)
    return sequences

def solve_commands_manual(path):
    # A = R,6,L,6,L,10,
    # B = L,8,L,6,L,10,L,6,
    # A = R,6,L,6,L,10,
    # B = L,8,L,6,L,10,L,6,
    # C = R,6,L,8,L,10,R,6,
    # A = R,6,L,6,L,10,
    # B = L,8,L,6,L,10,L,6,
    # C = R,6,L,8,L,10,R,6,
    # A = R,6,L,6,L,10,
    # C = R,6,L,8,L,10,R,6

    cmds = [
        "A,B,A,B,C,A,B,C,A,C",
        "R,6,L,6,L,10",
        "L,8,L,6,L,10,L,6",
        "R,6,L,8,L,10,R,6",
    ]

    return cmds


def solve_first_part(p):
    c = IntComputer(p)

    _map = ""
    halted = False
    while not halted:
        if c.pause:
            c.continue_program()
        else:
            c.run_program()

        if len(c.outputs) > 0:
            _map += chr(c.outputs.pop())

        if c.halted:
            halted = True

    print(_map)
    m = str_to_map(_map)
    intersections = find_intersections(m)
    c = calibrate(intersections)
    print(c)

    return m

def solve_second_part(p, cmds):
    p[0] = 2

    c = IntComputer(p)

    print(cmds)
    c.inputs = [ord(a) for a in cmds] + [10, ord('n'), 10]
    print(c.inputs)

    _map = ""
    halted = False
    while not halted:
        if c.pause:
            c.continue_program()
        else:
            c.run_program()

        if len(c.outputs) > 0:
            v = c.outputs.pop()
            if v < 256:
                _map += chr(v)

        if c.halted:
            halted = True

    print(_map)
    print(v)
    print(c.outputs)

def run_binary(p):
    m = solve_first_part(p)

    v = find_vaccumm_robots(m)
    path = find_path(v[0], m)
    print(path)
    print(len(path))

    cmds = solve_commands_manual(path)
    solve_second_part(p, "\n".join(cmds))


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]
        r = run_binary(p)

if __name__ == "__main__":
    main()