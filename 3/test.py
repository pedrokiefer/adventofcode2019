from main import (
    manhattan_distance,
    minimal_crossing_distance,
)


def test_manhattan_distance():
    p = (0, 0)
    q = (6, 6)

    d = manhattan_distance(p, q)
    assert d == 12


def test_example_1():
    path1 = "R8,U5,L5,D3"
    path2 = "U7,R6,D4,L4"

    d = minimal_crossing_distance(path1, path2)

    assert d == 6


def test_example_2():
    path1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    path2 = "U62,R66,U55,R34,D71,R55,D58,R83"

    d = minimal_crossing_distance(path1, path2)

    assert d == 159


def test_example_3():
    path1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    path2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

    d = minimal_crossing_distance(path1, path2)

    assert d == 135