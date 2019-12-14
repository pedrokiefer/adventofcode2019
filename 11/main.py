import itertools

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


def convert_modes(modes, size):
    modes = list(modes)
    m = [0] * size
    if len(modes) == 0:
        return [0] * size
    i = 0
    for i in range(size):
        if len(modes) > 0:
            m[i] = int(modes.pop(), 10)
    return m


class Memory(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        return super().__getitem__(index)


class OpCode:
    size = 0

    def __init__(self, sys, code, modes):
        self.sys = sys
        self.operation = code
        self.modes = convert_modes(modes, self.size - 1)

    def exec(self):
        raise NotImplementedError()

    def _value(self, p, mode, v):
        if mode == POSITION_MODE:
            return p[v]
        elif mode == IMMEDIATE_MODE:
            return v
        elif mode == RELATIVE_MODE:
            return p[self.sys.offset + v]

    def _value_set(self, p, mode, reg, v):
        if mode == POSITION_MODE:
            p[reg] = v
        elif mode == IMMEDIATE_MODE:
            print("?")
        elif mode == RELATIVE_MODE:
            p[self.sys.offset + reg] = v


class Add(OpCode):
    size = 4

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]
        result = self._value(p, self.modes[0], i1) + self._value(p, self.modes[1], i2)
        self._value_set(p, self.modes[2], reg, result)
        return self.size, p


class Multiply(OpCode):
    size = 4

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]
        result = self._value(p, self.modes[0], i1) * self._value(p, self.modes[1], i2)
        self._value_set(p, self.modes[2], reg, result)
        return self.size, p


class Input(OpCode):
    size = 2

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        # For now, we only have 1 input value
        # Make it a constant
        self._value_set(p, self.modes[0], i1, self.sys.input())
        return self.size, p


class Output(OpCode):
    size = 2

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        self.sys.output(self._value(p, self.modes[0], i1))
        return self.size, p


class JumpIfTrue(OpCode):
    size = 3

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        if self._value(p, self.modes[0], i1) != 0:
            return 0, p, self._value(p, self.modes[1], i2)
        return self.size, p


class JumpIfFalse(OpCode):
    size = 3

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        if self._value(p, self.modes[0], i1) == 0:
            return 0, p, self._value(p, self.modes[1], i2)
        return self.size, p


class LessThan(OpCode):
    size = 4

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]

        if self._value(p, self.modes[0], i1) < self._value(p, self.modes[1], i2):
            self._value_set(p, self.modes[2], reg, 1)
        else:
            self._value_set(p, self.modes[2], reg, 0)
        return self.size, p


class Equals(OpCode):
    size = 4

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]

        if self._value(p, self.modes[0], i1) == self._value(p, self.modes[1], i2):
            self._value_set(p, self.modes[2], reg, 1)
        else:
            self._value_set(p, self.modes[2], reg, 0)
        return self.size, p


class RelativeOffset(OpCode):
    size = 2

    def exec(self, p, op_pos):
        i1 = p[op_pos + 1]
        self.sys.offset += self._value(p, self.modes[0], i1)
        if self.sys.offset < 0:
            self.sys.offset = 0
        return self.size, p


class IntComputer:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.input_index = 0
        self.offset = 0
        self.halted = False
        self.pause = False

    def output(self, v):
        self.outputs.append(v)
        self.pause = True

    def input(self):
        if self.input_index < len(self.inputs):
            v = self.inputs[self.input_index]
            self.input_index += 1
            return v
        return 0

    def run_op_code(self, p, op_pos):
        op_value = str(p[op_pos])
        op = int(op_value[-2:], 10)
        modes = op_value[0:-2]

        if op == 1:
            return Add(self, op, modes).exec(p, op_pos)
        elif op == 2:
            return Multiply(self, op, modes).exec(p, op_pos)
        elif op == 3:
            return Input(self, op, modes).exec(p, op_pos)
        elif op == 4:
            return Output(self, op, modes).exec(p, op_pos)
        elif op == 5:
            return JumpIfTrue(self, op, modes).exec(p, op_pos)
        elif op == 6:
            return JumpIfFalse(self, op, modes).exec(p, op_pos)
        elif op == 7:
            return LessThan(self, op, modes).exec(p, op_pos)
        elif op == 8:
            return Equals(self, op, modes).exec(p, op_pos)
        elif op == 9:
            return RelativeOffset(self, op, modes).exec(p, op_pos)
        elif op == 99:
            self.halted = True
            return None, p
        else:
            # raise Exception(f"Invalid OpCode: {op}")
            return None, p

        return None, p

    def run_program(self, p):
        self.p = Memory(p)
        self.op_pos = 0

        self._run_loop()

    def _run_loop(self):
        inc_op = 0
        while True:
            result = self.run_op_code(self.p, self.op_pos)
            if len(result) == 2:
                inc_op, self.p = result
            else:
                inc_op, self.p, self.op_pos = result
                continue

            if inc_op is None:
                break
            else:
                self.op_pos += inc_op

            if self.pause:
                break

    def continue_program(self):
        self.pause = False
        self._run_loop()

DIRECTIONS = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}

def run_robot(p):
    c = IntComputer()
    board = {}

    x = 0
    y = 0
    f = 1

    painted = 0

    halted = False
    first_loop = True
    while not halted:
        should_halt = False

        c.input_index = 0
        if first_loop:
            c.inputs = [1]
        else:
            c.inputs = [board.get((x, y), (0, False))[0]]

        if c.pause:
            c.continue_program()
        else:
            c.run_program(p)

        if not c.halted:
            print(f"{x} {y} color: ", c.outputs)
            color = c.outputs.pop()
            c.continue_program()
            print(f"{x} {y} turn: ", c.outputs)
            turn = c.outputs.pop()
            s = board.get((x, y), (0, False))
            if s[1] == False:
                painted += 1
            board[(x, y)] = (color, True)
            if turn == 1:
                increment = 1
            else:
                increment = -1
            f = (f + increment) % 4
            d = DIRECTIONS[f]
            x += d[0]
            y += d[1]
        else:
            halted = True

    result = []
    for i in range(0, 41):
        line = ""
        for j in range(-6, 4):
            v = board.get((i, j), (0, False))
            if v[0] == 0:
                line += "."
            else:
                line += "#"
        result.append(line)

    s = "\n".join(result)
    print(s)

    return painted

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]
        r = run_robot(p)
        print(r)