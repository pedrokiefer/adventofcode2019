
def add(p, i1, i2, reg):
    p[reg] = p[i1] + p[i2]
    return 1


def multiply(p, i1, i2, reg):
    p[reg] = p[i1] * p[i2]
    return 1


def run_op_code(p, op_pos):
    op = p[op_pos]

    result = None
    if op == 1:
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]
        result = add(p, i1, i2, reg)
    elif op == 2:
        i1 = p[op_pos + 1]
        i2 = p[op_pos + 2]
        reg = p[op_pos + 3]
        result = multiply(p, i1, i2, reg)
    elif op == 99:
        return p, result
    else:
        return p, result

    return p, result


def run_program(p):
    op_pos = 0
    inc_op = 0
    while True:
        p, inc_op = run_op_code(p, op_pos)
        if inc_op is None:
            break
        else:
            op_pos += 4
    return p


def find_verb_and_noun(data, expected):
    for noun in range(0, 99):
        for verb in range(0, 99):
            i = data.copy()
            i[1] = noun
            i[2] = verb
            p = run_program(i)
            if p[0] == expected:
                return 100 * noun + verb


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]
        print(find_verb_and_noun(p, 19690720))

        #p = [int(x) for x in data.split(",")]
        #result = run_program(p)
        #print(",".join([str(x) for x in result]))
