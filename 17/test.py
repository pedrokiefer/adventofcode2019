from main import (
    str_to_map,
    print_map,
    find_bounds,
    find_intersections,
    calibrate,
    find_vaccumm_robots,
    find_path,
    solve_commands
)

def test_can_parse_string_map():
    input = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""
    m = str_to_map(input)
    s = print_map(m)
    bounds = find_bounds(m)

    intersections = find_intersections(m)

    c = calibrate(intersections)

    v = find_vaccumm_robots(m)
    p = find_path(v[0], m)

    assert s == input
    assert m[(2, 2)] == "#"
    assert bounds == (0, 12, 0, 6)
    assert intersections == [(2, 2), (2, 4), (6, 4), (10, 4)]
    assert c == 76
    assert v[0] == ((10, 6), "^")
    assert p == [
        "4", "R", "2", "R", "2", "R", "12",
        "R", "2", "R", "6", "R", "4", "R",
        "4", "R", "6"]

def test_path_2():
    input = """#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""

    m = str_to_map(input)
    v = find_vaccumm_robots(m)
    p = find_path(v[0], m)

    cmds = solve_commands(p)

    assert p == [
        "R", "8", "R", "8",
        "R", "4", "R", "4", "R", "8",
        "L", "6", "L", "2",
        "R", "4", "R", "4", "R", "8",
        "R", "8", "R", "8",
        "L", "6", "L", "2"]

    assert cmds == ["A,B,C,B,A,C", "R,8,R,8", "R,4,R,4,R,8", "L,6,L,2"]
