from .memory import Memory
from .opcodes import (
    Add,
    Multiply,
    Input,
    Output,
    JumpIfTrue,
    JumpIfFalse,
    LessThan,
    Equals,
    RelativeOffset
)


class IntComputer:
    def __init__(self, p):
        self.inputs = []
        self.outputs = []
        self.input_index = 0
        self.offset = 0
        self.halted = False
        self.pause = False

        self.p = Memory(p)
        self.op_pos = 0

    def output(self, v):
        self.outputs.append(v)

    def input(self):
        if self.input_index < len(self.inputs):
            v = self.inputs[self.input_index]
            self.input_index += 1
            return v
        return 0

    def run_op_code(self):
        op_value = str(self.p[self.op_pos])
        op = int(op_value[-2:], 10)
        modes = op_value[0:-2]

        if op == 1:
            return Add(self, op, modes).exec()
        elif op == 2:
            return Multiply(self, op, modes).exec()
        elif op == 3:
            return Input(self, op, modes).exec()
        elif op == 4:
            return Output(self, op, modes).exec()
        elif op == 5:
            return JumpIfTrue(self, op, modes).exec()
        elif op == 6:
            return JumpIfFalse(self, op, modes).exec()
        elif op == 7:
            return LessThan(self, op, modes).exec()
        elif op == 8:
            return Equals(self, op, modes).exec()
        elif op == 9:
            return RelativeOffset(self, op, modes).exec()
        elif op == 99:
            self.halted = True
            return None
        else:
            # raise Exception(f"Invalid OpCode: {op}")
            return None

        return None

    def run_program(self):
        self.op_pos = 0
        self._run_loop()

    def _run_loop(self):
        inc_op = 0
        while True:
            inc_op = self.run_op_code()

            if inc_op is None:
                break
            else:
                self.op_pos += inc_op

            if self.pause:
                break

    def continue_program(self):
        self.pause = False
        self._run_loop()