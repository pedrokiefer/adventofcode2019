import numpy as np
from intcode import IntComputer

def find_bounds(m):
    keys = list(m.keys())

    xmin = min(keys)[0]
    xmax = max(keys)[0]

    ymin = min(keys)[1]
    ymax = max(keys)[1]

    return xmin, xmax, ymin, ymax


def print_map(m):
    xmin, xmax, ymin, ymax = find_bounds(m)

    lines = []
    for y in range(ymin, ymax + 1):
        l = ""
        for x in range(xmin, xmax + 1):
            v = m.get((x, y), None)
            if v:
                l += str(v)
        lines.append(l)

    return "\n".join(lines)


def tractor_beam(x, y, p):
    c = IntComputer(p)

    c.inputs = [x, y]

    result = 0
    halted = False
    while not halted:
        if c.pause:
            c.continue_program()
        else:
            c.run_program()

        if len(c.outputs) > 0:
            result = c.outputs.pop()

        if c.halted:
            halted = True
    return result

def scan_tractor_area(p):
    count = 0
    m = {}
    for x in range(0, 50):
        for y in range(0, 50):
            t = tractor_beam(x, y, p)
            if t == 0:
                m[(x, y)] = "."
            else:
                count += 1
                m[(x, y)] = "#"

    print(print_map(m))
    return count

def scan_line(y, p):
    last_t = 0
    last_point = 0
    for x in range(0, y):
        t = tractor_beam(x, y, p)
        if last_t == 0 and t == 1:
            last_t = t
            first_point = (x, y)
            continue
        elif last_t == 1 and t == 0:
            last_t = t
            last_point = (x, y)
            break
        else:
            last_t = t
    return (first_point, last_point)

def tractor_beam_angle(p):
    first_point, last_point = scan_line(100, p)

    # Get angles
    angle1 = np.arctan(first_point[0] / first_point[1])
    angle2 = np.arctan(last_point[0] / last_point[1])

    # Get beam angle
    beam_angle = (angle2 - angle1) / (1 + angle1 * angle2)
    print(beam_angle)

    # For beam angle, find square diagonal
    # assuming line is perpendicular
    l = 100 * np.sqrt(2) / np.tan(beam_angle)
    print(l)
    v1 = (int(l * np.cos(angle1)), int(l * np.sin(angle1)))
    print(v1)

    x = 0
    y = 0
    run = True
    while run:
        while True:
            t1 = tractor_beam(x + 99, y, p)
            print(f"t1: {t1} ({x + 99}, {y})")
            if t1 == 1:
                t2 = tractor_beam(x, y + 99, p)
                print(f"t2: {t2} ({x}, {y + 99})")
                if t2 == 1:
                    run = False
                    break
                break
            y += 1
        if not run:
            break
        x += 1
    print(x, y)
    print(10000 * x + y)

    print(scan_line(v1[1], p))
    print(scan_line(v1[1] - 99, p))

    print(first_point, last_point)
    print(angle1, angle2)


def run_binary(p):
    #count = scan_tractor_area(p)
    #print(count)

    beam_angles = tractor_beam_angle(p)



def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        p = [int(x) for x in data.split(",")]
        r = run_binary(p)

if __name__ == "__main__":
    main()