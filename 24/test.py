from main import (
    parse_map,
    print_map,
    step_bugs,
    find_repeated_pattern,
    biodiversity_rating,
    infinity_map_run
)

def test_can_step_state_1m():
    input = """....#
#..#.
#..##
..#..
#...."""
    m = parse_map(input)
    r = step_bugs(m)
    output = print_map(r)

    print(output)

    assert output == """#..#.
####.
###.#
##.##
.##.."""

def test_can_step_state_2m():
    input = """....#
#..#.
#..##
..#..
#...."""
    m = parse_map(input)
    r = step_bugs(m)
    r = step_bugs(r)
    output = print_map(r)

    print(output)

    assert output == """#####
....#
....#
...#.
#.###"""

def test_can_step_state_3m():
    input = """....#
#..#.
#..##
..#..
#...."""
    m = parse_map(input)
    r = step_bugs(m)
    r = step_bugs(r)
    r = step_bugs(r)
    output = print_map(r)

    print(output)

    assert output == """#....
####.
...##
#.##.
.##.#"""

def test_can_step_state_4m():
    input = """....#
#..#.
#..##
..#..
#...."""
    m = parse_map(input)
    r = step_bugs(m)
    r = step_bugs(r)
    r = step_bugs(r)
    r = step_bugs(r)
    output = print_map(r)

    print(output)

    assert output == """####.
....#
##..#
.....
##..."""

def test_can_find_pattern():
    input = """....#
#..#.
#..##
..#..
#...."""
    m = parse_map(input)
    r = find_repeated_pattern(m)
    rating = biodiversity_rating(r)
    output = print_map(r)

    print(output)

    assert output == """.....
.....
.....
#....
.#..."""
    assert rating == 2129920

def test_infinity_after_10min():
    input = """....#
#..#.
#..##
..#..
#...."""

    m = parse_map(input)
    r = infinity_map_run(m, 10)
    output = print_map(r)

    assert output == """.#...
.#.##
.#...
.....
....."""