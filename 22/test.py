from main import (
    new_deck,
    new_stack,
    cut,
    increment,
    slam_shuffle
)

def test_new_stack():
    d = new_deck(10)
    d = new_stack(d)

    assert d == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def test_cut_deck():
    d = new_deck(10)
    d = cut(d, 3)

    assert d == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

def test_cut_deck_negative():
    d = new_deck(10)
    d = cut(d, -4)

    assert d == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

def test_increment():
    d = new_deck(10)
    d = increment(d, 3)

    assert d == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

def test_shuffle_1():
    input = """deal with increment 7
deal into new stack
deal into new stack"""

    result, n = slam_shuffle(input, 10)
    assert result == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

def test_shuffle_2():
    input = """cut 6
deal with increment 7
deal into new stack"""

    result, n = slam_shuffle(input, 10)
    assert result == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

def test_shuffle_3():
    input = """deal with increment 7
deal with increment 9
cut -2"""

    result, n = slam_shuffle(input, 10)
    assert result == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

def test_shuffle_4():
    input = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

    result, n = slam_shuffle(input, 10)
    assert result == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]