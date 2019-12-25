from intcode import IntComputer
from queue import Queue

COMMAND_NORTH = 1
COMMAND_SOUTH = 2
COMMAND_WEST = 3
COMMAND_EAST = 4

CMD_TO_STR = {
    COMMAND_NORTH: "N",
    COMMAND_SOUTH: "S",
    COMMAND_EAST: "E",
    COMMAND_WEST: "W",
}

CMDS_LIST = [COMMAND_NORTH, COMMAND_EAST, COMMAND_SOUTH, COMMAND_WEST]

WALL = 0
MOVED = 1
OXYGEN_SYSTEM = 2

VALID_MOVES = {
    COMMAND_NORTH: (0, 1),
    COMMAND_SOUTH: (0, -1),
    COMMAND_WEST: (-1, 0),
    COMMAND_EAST: (1, 0),
}

OPPOSITE = {
    COMMAND_NORTH: COMMAND_SOUTH,
    COMMAND_SOUTH: COMMAND_NORTH,
    COMMAND_WEST: COMMAND_EAST,
    COMMAND_EAST: COMMAND_WEST,
}


class Tile:
    visited = [False, False, False, False]
    kind = " "

    def __init__(self, kind):
        self.kind = kind

    def __str__(self):
        return f"<{self.kind} visited={self.visited}>"


def not_visited(v, tx, ty):
    print(f"({tx}, {ty}) -> {v}")
    if v.kind == "#":
        return False

    for i in range(4):
        if not v.visited[i]:
            return True
    return False


def get_next_cmd(board, cmd, x, y):
    next_cmd = cmd

    for t in range(4):
        next_cmd = (next_cmd + 1) % 4

        m = VALID_MOVES[CMDS_LIST[next_cmd]]
        tx = x + m[0]
        ty = y + m[1]

        v = board.get((tx, ty), None)
        if v == None or not_visited(v, tx, ty):
            break

    if next_cmd == cmd:
        print("reverse")
        return (next_cmd + 2) % 4

    return next_cmd


def print_board(board):
    lines = []
    for i in range(-20, 23):
        l = ""
        for j in range(-22, 21):
            v = board.get((j, i), None)
            if v is None:
                l += " "
            elif v == 0:
                l += "#"
            elif v == 1:
                l += "."
            elif v == 2:
                l += "O"
        lines.append(l)
    lines.reverse()
    return "\n".join(lines)


def point_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def step(c, d):
    c.input_index = 0
    c.inputs = [d]

    if c.pause:
        c.continue_program()
    else:
        c.run_program()

    return c.outputs.pop()


def visit_nodes(c, board, n):
    for d, m in VALID_MOVES.items():
        next_point = point_add(n, m)
        t = board.get(next_point, None)
        if t:
            continue
        o = step(c, d)
        board[next_point] = o
        if o == WALL:
            continue
        visit_nodes(c, board, next_point)
        step(c, OPPOSITE[d])


def find_oxygen(board):
    for p, v in board.items():
        if v == 2:
            return p
    return None


def all_paths_from(board, p1):
    paths = {}
    visited = []

    q = []
    q.append((p1, 0))

    while len(q) > 0:
        point, d = q[0]
        q = q[1:]
        paths[point] = d

        for direction, m in VALID_MOVES.items():
            np = point_add(point, m)
            if np in visited:
                continue
            visited.append(np)
            if board[np] != WALL:
                #d.append(direction)
                q.append((np, d + 1))

    return paths

def shortest_path(board, p1, p2):
    paths = all_paths_from(board, p1)
    return paths[p2]

def longest_path(board, p1):
    paths = all_paths_from(board, p1)
    return max(paths.values())

def run_game(p):
    c = IntComputer(p)
    board = {}

    x = 0
    y = 0

    board[(x, y)] = Tile(".")

    halted = False
    first_loop = True
    next_cmd = 0
    counter = 0

    visit_nodes(c, board, (0, 0))
    o_point = find_oxygen(board)

    print(print_board(board))

    print(o_point)
    min_dist = shortest_path(board, (0, 0), o_point)
    print(min_dist)
    print(longest_path(board, o_point))

    # while not halted:
    #     should_halt = False

    #     c.input_index = 0
    #     c.inputs = [CMDS_LIST[next_cmd]]

    #     if c.pause:
    #         c.continue_program()
    #     else:
    #         c.run_program()

    #     if counter != 0 and counter % 10 == 0:
    #         print_board(board)

    #     counter += 1

    #     if not c.halted:
    #         output = c.outputs.pop()

    #         if output == MOVED:
    #             m = VALID_MOVES[CMDS_LIST[next_cmd]]

    #             board[(x, y)].visited[next_cmd] = True

    #             x += m[0]
    #             y += m[1]
    #             print(f"m ({x}, {y}) = '.'")

    #             t = Tile(".")
    #             t.visited[(next_cmd - 1) % 4] = True
    #             board[(x, y)] = t

    #         if output == WALL:
    #             m = VALID_MOVES[CMDS_LIST[next_cmd]]
    #             tx = x + m[0]
    #             ty = y + m[1]
    #             board[(x, y)].visited[next_cmd] = True

    #             t = Tile("#")
    #             t.visited[(next_cmd - 1) % 4] = True
    #             board[(tx, ty)] = t
    #             print(f"w ({tx}, {ty}) = '#'")

    #         if output == OXYGEN_SYSTEM:
    #             print(f"({x}, {y}) = 'O'")
    #             m = VALID_MOVES[CMDS_LIST[next_cmd]]
    #             x += m[0]
    #             y += m[1]

    #             board[(x, y)] = "O"
    #             halted = True

    #         print(f"w cur_cmd = {CMD_TO_STR[CMDS_LIST[next_cmd]]}")
    #         next_cmd = get_next_cmd(board, next_cmd, x, y)
    #         print(f"w next_cmd = {CMD_TO_STR[CMDS_LIST[next_cmd]]}\n===")
    #     else:
    #         halted = True

    print(print_board(board))
    return 0


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]
        r = run_game(p)
