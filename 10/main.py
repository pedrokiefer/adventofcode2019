from math import sqrt, isclose
from collections import namedtuple
import numpy as np

ASTEROID_MARK = "#"


def to_grid(asteroids):
    g = {}
    asteroids = asteroids.split("\n")

    height = len(asteroids)
    width = len(asteroids[0])
    for y, l in enumerate(asteroids):
        for x, v in enumerate(l):
            g[(x, y)] = v
    return g, (width, height)


def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def vector(p1, p2):
    v = ((p2[0] - p1[0]), (p2[1] - p1[1]))
    d = sqrt(v[0] ** 2 + v[1] ** 2)
    return (round(v[0] / d, 8), round(v[1] / d, 8))


Viewed = namedtuple("Viewed", ["vector", "distance", "asteroid"])


def asteroids_in_view(point, asteroids):
    viewed_dict = {}
    for a in asteroids:
        if a[0] == point[0] and a[1] == point[1]:
            continue

        v = vector(a, point)
        d = distance(a, point)

        viewed = Viewed(v, d, a)

        if v not in viewed_dict:
            viewed_dict[v] = viewed
        else:
            old = viewed_dict[v]
            if viewed.distance < old.distance:
                viewed_dict[v] = viewed

    return len(viewed_dict.values()), list(viewed_dict.values())


def print_grid(g, dimension):
    r = ""
    for i in range(dimension[1]):
        l = ""
        for j in range(dimension[0]):
            v = g.get((j, i), None)
            if v:
                l += str(v[0])
            else:
                l += "."
        r += l + "\n"
    return r


def by_angle(viewed):
    up = np.array([0, 1])
    vector = np.array(viewed.vector)
    angle = np.arctan2(np.linalg.det([up, vector]), np.dot(up, vector))
    return angle


def scan_asteroids(asteroids_stream):
    g, d = to_grid(asteroids_stream)

    result = {}
    asteroids = list(
        filter(lambda x: x, [k if v == ASTEROID_MARK else None for k, v in g.items()])
    )
    for a in asteroids:
        view = asteroids_in_view(a, asteroids)
        result[a] = view

    return result, d


def find_best_placement(g):
    m = max(g.items(), key=lambda x: x[1][0])[0]
    print(f"{m} -> {g[m][0]}")
    return m


def destroy_order(g, m):
    found = g[m][1]
    found.sort(key=by_angle)
    sign_change = 0
    for i, v in enumerate(found):
        if v.vector == (0, 1):
            sign_change = i
    found = found[sign_change:] + found[:sign_change]
    return found


def get_200th_value(found):
    if len(found) < 199:
        return 0
    p = found[199].asteroid
    r = p[0] * 100 + p[1]
    return r


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    g, d = scan_asteroids(data)
    m = find_best_placement(g)
    t = destroy_order(g, m)
    value = get_200th_value(t)
    print(value)


if __name__ == "__main__":
    main()
