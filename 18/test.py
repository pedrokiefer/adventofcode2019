from main import (
    parse_map,
    find_entrance,
    all_paths_from,
    collect_keys
)


def test_can_parse_map():
    input = """#########
#b.A.@.a#
#########"""
    m = parse_map(input)

    assert m[(5,1)] == "@"

def test_get_all_paths():
    input = """#########
#b.A.@.a#
#########"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    assert m[(5,1)] == "@"
    assert keys == {
        'a': [(1, 0), (1, 0)],
    }
    assert doors == {'A': [(-1, 0), (-1, 0)]}
    assert paths == {
        (3, 1): [(-1, 0), (-1, 0)],
        (4, 1): [(-1, 0)],
        (5, 1): [],
        (6, 1): [(1, 0)],
        (7, 1): [(1, 0), (1, 0)]
    }

def test_min_path():
    input = """#########
#b.A.@.a#
#########"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    min_steps, ck = collect_keys(m)

    assert min_steps == 8
    assert ck == ["a", "b"]

def test_min_longer_path():
    input = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    min_steps, ck = collect_keys(m)

    assert min_steps == 86
    assert ck == ["a", "b", "c", "d", "e", "f"]

def test_min_longer_path_2():
    input = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    min_steps, ck = collect_keys(m)

    assert min_steps == 132
    assert ck == ["b", "a", "c", "d", "f", "e", "g"]


def test_min_longer_path_3():
    input = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    min_steps, ck = collect_keys(m)

    assert min_steps == 136
    assert ck == ["a", "f", "b", "j", "g", "n", "h", "d", "l", "o", "e", "p", "c", "i", "k", "m"]


def test_min_longer_path_4():
    input = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
    m = parse_map(input)
    paths, keys, doors = all_paths_from(m, find_entrance(m))

    min_steps, ck = collect_keys(m)

    assert min_steps == 81
    assert ck == ["a", "c", "f", "i", "d", "g", "b", "e", "h"]
