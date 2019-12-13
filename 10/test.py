from main import (
    scan_asteroids,
    find_best_placement,
    destroy_order,
    get_200th_value,
    print_grid,
)

def test_scan_asteroids():
    asteroids = """.#..#
.....
#####
....#
...##"""
    expected = """.7..7
.....
67775
....7
...87
"""
    result, d = scan_asteroids(asteroids)
    r = print_grid(result, d)
    assert r == expected

def test_scan_asteroids_placement():
    asteroids = """.#..#
.....
#####
....#
...##"""
    expected = """.7..7
.....
67775
....7
...87
"""
    result, d = scan_asteroids(asteroids)
    m = find_best_placement(result)
    r = print_grid(result, d)
    assert r == expected
    assert m == (3, 4)

def test_destroy_order():
    input = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""
    result, d = scan_asteroids(input)
    m = find_best_placement(result)
    t = destroy_order(result, m)
    asteroids = [v.asteroid for v in t]
    print(asteroids)
    assert asteroids == [
        (8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1),
        (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4),
        (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2), (1, 0), (5, 1),
        (6, 1), (6, 0), (7, 0)
    ]

def test_best_station():
    input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    result, d = scan_asteroids(input)
    m = find_best_placement(result)
    assert m == (11, 13)
    assert result[m][0] == 210


def test_best_station_destroy():
    input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    result, d = scan_asteroids(input)
    m = find_best_placement(result)
    t = destroy_order(result, m)
    v = get_200th_value(t)
    assert m == (11, 13)
    assert result[m][0] == 210
    assert v == 802