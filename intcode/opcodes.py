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

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        reg = self.sys.p[self.sys.op_pos + 3]
        result = self._value(self.sys.p, self.modes[0], i1) + self._value(
            self.sys.p, self.modes[1], i2
        )
        self._value_set(self.sys.p, self.modes[2], reg, result)
        return self.size


class Multiply(OpCode):
    size = 4

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        reg = self.sys.p[self.sys.op_pos + 3]
        result = self._value(self.sys.p, self.modes[0], i1) * self._value(self.sys.p, self.modes[1], i2)
        self._value_set(self.sys.p, self.modes[2], reg, result)
        return self.size


class Input(OpCode):
    size = 2

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        # For now, we only have 1 input value
        # Make it a constant
        self._value_set(self.sys.p, self.modes[0], i1, self.sys.input())
        return self.size


class Output(OpCode):
    size = 2

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        self.sys.output(self._value(self.sys.p, self.modes[0], i1))
        return self.size


class JumpIfTrue(OpCode):
    size = 3

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        if self._value(self.sys.p, self.modes[0], i1) != 0:
            self.sys.op_pos = self._value(self.sys.p, self.modes[1], i2)
            return 0
        return self.size


class JumpIfFalse(OpCode):
    size = 3

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        if self._value(self.sys.p, self.modes[0], i1) == 0:
            self.sys.op_pos = self._value(self.sys.p, self.modes[1], i2)
            return 0
        return self.size


class LessThan(OpCode):
    size = 4

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        reg = self.sys.p[self.sys.op_pos + 3]

        if self._value(self.sys.p, self.modes[0], i1) < self._value(self.sys.p, self.modes[1], i2):
            self._value_set(self.sys.p, self.modes[2], reg, 1)
        else:
            self._value_set(self.sys.p, self.modes[2], reg, 0)
        return self.size


class Equals(OpCode):
    size = 4

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        i2 = self.sys.p[self.sys.op_pos + 2]
        reg = self.sys.p[self.sys.op_pos + 3]

        if self._value(self.sys.p, self.modes[0], i1) == self._value(self.sys.p, self.modes[1], i2):
            self._value_set(self.sys.p, self.modes[2], reg, 1)
        else:
            self._value_set(self.sys.p, self.modes[2], reg, 0)
        return self.size


class RelativeOffset(OpCode):
    size = 2

    def exec(self):
        i1 = self.sys.p[self.sys.op_pos + 1]
        self.sys.offset += self._value(self.sys.p, self.modes[0], i1)
        if self.sys.offset < 0:
            self.sys.offset = 0
        return self.size
