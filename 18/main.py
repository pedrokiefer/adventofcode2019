UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"

WALL = "#"

DIRECTIONS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
}

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


def find_entrance(map):
    for p, v in map.items():
        if v == "@":
            return p
    return None


def point_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def move(p1, points):
    p = p1
    print(p, points)
    for p2 in points:
        p = point_add(p, p2)
    return p


def all_paths_from(board, p1):
    paths = {}
    visited = [p1]
    keys = {}
    doors = {}

    q = []
    q.append((p1, list(), False))

    while len(q) > 0:
        point, d, block = q[0]
        q = q[1:]
        paths[point] = d

        if block:
            continue

        # print(f"=== {q} === {visited}")
        for direction, m in DIRECTIONS.items():
            np = point_add(point, m)
            if np in visited:
                continue
            visited.append(np)
            v = board[np]
            if v != WALL:
                nd = list(d)
                nd.append(m)
                # print(f"point: {point}, np: {np}, d:{nd}")
                if not str.isalpha(v):
                    q.append((np, nd, False))
                    continue
                if str.islower(v):
                    q.append((np, nd, True))
                    keys[v] = nd
                    continue
                if str.isupper(v):
                    q.append((np, nd, True))
                    doors[v] = nd
                    continue

    return paths, keys, doors


def next_key(keys, p):
    result = None
    lens = {k: len(v) for k, v in keys.items()}
    for k, path in keys.items():
        result = k
    return result


def has_doors(doors, collected_keys):
    for d in doors.keys():
        if d.upper() in collected_keys:
            return True
    return False

def find_items(m, func):
    items = {}
    for k, v in m.items():
        if func(v):
            items[v] = k
    return items


def collect_keys(m):
    p = find_entrance(m)

    collected_keys = []
    all_keys = find_items(m, lambda v: str.isalpha(v) and str.islower(v))
    all_doors = find_items(m, lambda v: str.isalpha(v) and str.isupper(v))

    m[p] = "."
    length = 0
    has_keys = True
    while has_keys:
        print(print_map(m))
        paths, keys, doors = all_paths_from(m, p)
        if len(keys) == 0 and not has_doors(doors, collected_keys):
            break

        nkey = next_key(keys, p)
        collected_keys.append(nkey)
        length += len(keys[nkey])
        p = move(p, keys[nkey])
        print(f"key: {p}")
        m[p] = "."
        door = all_doors.get(nkey.upper())
        if door:
            m[door] = "."


    print(collected_keys)
    print(length)
    return length, collected_keys