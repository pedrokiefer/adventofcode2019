
from main import run_program


def test_simple_program():
    program = [1, 0, 0, 0, 99]
    result = run_program(program)
    assert result == [2, 0, 0, 0, 99]


def test_multiply_program():
    program = [2, 3, 0, 3, 99]
    result = run_program(program)
    assert result == [2, 3, 0, 6, 99]


def test_complex_1():
    program = [2, 4, 4, 5, 99, 0]
    result = run_program(program)
    assert result == [2, 4, 4, 5, 99, 9801]


def test_complex_2():
    program = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    result = run_program(program)
    assert result == [30, 1, 1, 4, 2, 5, 6, 0, 99]
