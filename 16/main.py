from functools import lru_cache
import math

@lru_cache(maxsize=1024*1000)
def gen_pattern(element, length):
    base_phase = [0, 1, 0, -1]
    result = []
    l = 0

    while l < length:
        for j in range(4):
            for i in range(element):
                result.append(base_phase[j])
                l += 1

    return result[1:]

def multiply(input, p):
    r = 0
    for i, v in enumerate(input):
        r += int(v) * p[i]
    return str(r)[-1]


@lru_cache(maxsize=1024*1000)
def calculate_phase(input):
    result = []
    l = len(input)
    for i in range(l):
        p = gen_pattern(i + 1, l + 1)
        r = multiply(input, p)
        result.append(r)

    return "".join(result)

def calc_multiple_phases(phases, input):
    for i in range(phases):
        input = calculate_phase(input)
    return input

def msg_from_offset(input, offset, repeat, phases):
    r = []
    for i in range(len(input) * repeat - offset):
        r.append(int(input[(offset + i) % len(input)]))
    return r


def calc_with_offset(input, repeat, phases):
    msg = msg_from_offset(input, int(input[:7], 10), repeat, phases)
    n = len(msg)

    for p in range(phases):
        s = 0
        for i in range(n):
            s += msg[i]
            msg[i] = abs(s) % 10
    return "".join([str(d) for d in msg[:8]])

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    r = calc_multiple_phases(100, data)
    print(r[:8])

def main2():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

    print(calc_with_offset(data, 10000, 100))

if __name__ == "__main__":
    main2()