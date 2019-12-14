from main import (
    create_moon,
    parse_input,
    step,
    simulate_moons
)


def test_can_create_moon():
    input = "<x=-1, y=0, z=2>"
    m = create_moon(input)
    assert m.position == [-1, 0, 2]
    assert str(m) == "pos=<x=-1, y=0, z=2>, vel=<x=0, y=0, z=0>"

def test_step_moons():
    input = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moons = parse_input(input)
    step(moons)
    assert moons[0].position == [2, -1, 1]
    assert moons[1].position == [3, -7, -4]
    assert moons[2].position == [1, -7, 5]
    assert moons[3].position == [2, 2, 0]

    assert moons[0].velocity == [3, -1, -1]
    assert moons[1].velocity == [1, 3, 3]
    assert moons[2].velocity == [-3, 1, -3]
    assert moons[3].velocity == [-1, -3, 1]

def test_step_10x_moons():
    input = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moons = parse_input(input)
    r = simulate_moons(moons, 10)

    assert moons[0].position == [2, 1, -3]
    assert moons[1].position == [1, -8, 0]
    assert moons[2].position == [3, -6, 1]
    assert moons[3].position == [2, 0, 4]

    assert moons[0].velocity == [-3, -2, 1]
    assert moons[1].velocity == [-1, 1, 3]
    assert moons[2].velocity == [3, 2, -3]
    assert moons[3].velocity == [1, -1, -1]

    assert r == 179