from main import (
    calculate_orbits,
    input_to_tree,
    you_to_santa_path,
)

def test_simple_orbits():
    input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

    orbits = calculate_orbits(input)
    assert orbits == 42


def test_santa_path():
    input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
    t = input_to_tree(input)
    path_len = you_to_santa_path(t)
    assert path_len == 4