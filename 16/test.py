from main import (
    gen_pattern,
    multiply,
    calculate_phase,
    calc_with_offset,
    calc_multiple_phases,
)

def test_gen_pattern():
    phase = gen_pattern(2, 15)

    assert phase == [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]

def test_multiply():
    r = multiply("12345678", [1, 0, -1, 0, 1, 0, -1, 0])
    assert r == "4"

def test_can_calculate_phase():
    r = calculate_phase("12345678")
    assert r == "48226158"

def test_can_calculate_multiple_phases():
    r = calc_multiple_phases(4, "12345678")
    assert r == "01029498"

def test_can_calculate_multiple_phases_long_1():
    r = calc_multiple_phases(100, "80871224585914546619083218645595")
    assert r[:8] == "24176176"

def test_can_calculate_multiple_phases_long_2():
    r = calc_multiple_phases(100, "19617804207202209144916044189917")
    assert r[:8] == "73745418"

def test_can_calculate_multiple_phases_long_3():
    r = calc_multiple_phases(100, "69317163492948606335995924319873")
    assert r[:8] == "52432133"

def test_can_calculate_with_offset():
    r = calc_with_offset("03036732577212944063491565474664", 10000, 100)

    assert r == "84462026"