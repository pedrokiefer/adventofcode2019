UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"

DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
}

TILE_BUG = "#"
TILE_EMPTY = "."

def find_bounds(m):
    keys = list(m.keys())

    xmin = min(keys)[0]
    xmax = max(keys)[0]

    ymin = min(keys)[1]
    ymax = max(keys)[1]

    return xmin, xmax, ymin, ymax


def parse_map(input):
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

def is_bug(m, p, depth, d):
    tile = m.get(point_add(p, DIRECTIONS[d]))
    if not tile:
        return 0

    if tile == TILE_EMPTY:
        return 0

    if tile == TILE_BUG:
        return 1
    return 0

def bug_or_not(m, p, depth):
    s = sum([
        is_bug(m, p, depth, d)
        for d in DIRECTIONS.keys()
    ])
    v = m[p]
    if v == TILE_BUG:
        if s == 1:
            return TILE_BUG
        return TILE_EMPTY
    elif v == TILE_EMPTY:
        if s == 1 or s == 2:
            return TILE_BUG
        return TILE_EMPTY


def step_bugs(m, depth=0):
    xmin, xmax, ymin, ymax = find_bounds(m)

    new_map = {}

    for y in range(xmax + 1):
        for x in range(ymax + 1):
            new_map[(x, y)] = bug_or_not(m, (x, y), depth)

    return new_map

def find_repeated_pattern(m):
    maps = [print_map(m)]

    count = 0
    while True:
        m = step_bugs(m)
        mstr = print_map(m)
        if mstr in maps:
            break
        count += 1
        maps.append(mstr)
    print(count)
    return m

def biodiversity_rating(m):
    xmin, xmax, ymin, ymax = find_bounds(m)

    p = 0
    r = 0

    for y in range(xmax + 1):
        for x in range(ymax + 1):
            if m[(x, y)] == TILE_BUG:
                r += 2 ** p
            p += 1
    return r

def infinity_map_run(m, time):
    for i in range(time):
        m = step_bugs(m)
    return m

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        m = parse_map(data)
        m = find_repeated_pattern(m)
        print(biodiversity_rating(m))


if __name__ == "__main__":
    main()