from intcode import IntComputer

def run_springscript(p, script):
    c = IntComputer(p)

    c.inputs = [ord(a) for a in script]
    print(c.inputs)

    _map = ""
    halted = False
    while not halted:
        if c.pause:
            c.continue_program()
        else:
            c.run_program()

        if len(c.outputs) > 0:
            v = c.outputs.pop()
            if v < 256:
                _map += chr(v)

        if c.halted:
            halted = True

    print(_map)
    print(v)

    return v

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]

        script1 = [
            "NOT A J",
            "NOT C T",
            "AND D T",
            "OR T J",
            "WALK\n"
        ]
        r = run_springscript(p, "\n".join(script1))
        print(f"part 1: {r}")

        script2 = [
            "NOT C T",
            "NOT B J",
            "OR T J",
            "NOT A T",
            "OR T J",
            "OR E T",
            "OR H T",
            "AND D T",
            "AND T J",
            "RUN\n"
        ]
        r = run_springscript(p, "\n".join(script2))
        print(f"part 2: {r}")

if __name__ == "__main__":
    main()