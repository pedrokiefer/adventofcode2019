
DIRECTIONS = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def manhattan_distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def path_to_cmds(p):
    return [(cmd[0], int(cmd[1:])) for cmd in p.split(",")]


def points(cmds):
    points = {}

    x = 0
    y = 0
    steps = 0

    for direction, dist in cmds:
        for point in range(dist):
            dx, dy = DIRECTIONS[direction]
            x += dx
            y += dy
            steps += 1
            points[(x, y)] = steps
    return points


def path_intersects(p1, p2):
    return set(p1.keys()).intersection(set(p2.keys()))

def get_intersections(p1, p2):
    cmds1 = path_to_cmds(p1)
    p1 = points(cmds1)
    cmds2 = path_to_cmds(p2)
    p2 = points(cmds2)

    intersections = path_intersects(p1, p2)

    return intersections, p1, p2

def minimal_crossing_distance(intersections):
    distances = []
    for i in intersections:
        distances.append(manhattan_distance((0, 0), i))

    return min(distances)

def get_least_steps(intersections, points1, points2):
    return [points1[point] + points2[point] for point in intersections]

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        line1 = f.readline()
        line2 = f.readline()

        intersections, p1, p2 = get_intersections(line1.strip(), line2.strip())
        print(minimal_crossing_distance(intersections))
        print(min(get_least_steps(intersections, p1, p2)))
