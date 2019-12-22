from unittest.mock import Mock

from .cpu import IntComputer

def test_simple_program():
    program = [1, 0, 0, 0, 99]
    c = IntComputer(program)
    c.run_program()
    assert c.p == [2, 0, 0, 0, 99]


def test_multiply_program():
    program = [2, 3, 0, 3, 99]
    c = IntComputer(program)
    c.run_program()
    assert c.p == [2, 3, 0, 6, 99]


def test_complex_1():
    program = [2, 4, 4, 5, 99, 0]
    c = IntComputer(program)
    c.run_program()
    assert c.p == [2, 4, 4, 5, 99, 9801]


def test_complex_2():
    program = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    c = IntComputer(program)
    c.run_program()
    assert c.p == [30, 1, 1, 4, 2, 5, 6, 0, 99]

def test_complex_3():
    program = [1101, 100, -1, 4, 0]
    c = IntComputer(program)
    c.run_program()
    assert c.p == [1101, 100, -1, 4, 99]

def test_position_mode_input_equals_8():
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    c = IntComputer(program)
    def output(a):
        assert a == 1
    def input():
        return 8
    c.output = output
    c.input = input
    c.run_program()
    assert c.p == [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8]


def test_position_mode_input_less_than_8():
    program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    c = IntComputer(program)
    def output(a):
        assert a == 0
    def input():
        return 8
    c.output = output
    c.input = input
    c.run_program()
    assert c.p == [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8]


def test_immediate_mode_input_equals_8():
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    c = IntComputer(program)
    def output(a):
        assert a == 1
    def input():
        return 8
    c.output = output
    c.input = input
    c.run_program()
    assert c.p == [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8]


def test_immediate_mode_input_less_than_8():
    program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    c = IntComputer(program)
    def output(a):
        assert a == 0
    def input():
        return 8
    c.output = output
    c.input = input
    c.run_program()
    assert c.p == [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8]


def test_offset_1():
    program = [109, 19, 99]
    c = IntComputer(program)
    c.offset = 2000
    c.output = Mock()
    c.run_program()
    assert c.offset == 2019


def test_offset_2():
    program = [109, 19, 204, -34, 99]
    c = IntComputer(program)
    c.offset = 2000
    c.output = Mock()
    c.run_program()
    assert c.offset == 2019
    assert c.output.call_count == 1

def test_quine():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    c = IntComputer(program)
    c.output = Mock()
    c.run_program()
    assert c.output.call_count == 16
    call_values = [call[0][0] for call in c.output.call_args_list]
    assert call_values == [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]


def test_16bit_number():
    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    c = IntComputer(program)

    def output(a):
        assert a == 1219070632396864

    c.output = output
    c.run_program()


def test_print_large_number():
    program = [104, 1125899906842624, 99]
    c = IntComputer(program)

    def output(a):
        assert a == 1125899906842624

    def input():
        return 8

    c.output = output
    c.input = input
    c.run_program()

