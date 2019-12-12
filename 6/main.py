class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def print(self):
        print(self)
        if self.children:
            for c in self.children:
                c.print()

    def count(self):
        v = len(self.children)
        for c in self.children:
            v += c.count()
        return v

    def _count(self):
        if self.parent:
            return 1 + self.parent._count()
        return 0

    def parents(self):
        if self.parent:
            return [self.parent.name, *self.parent.parents()]
        return []

    def __str__(self):
        if self.parent and self.children:
            return f"{self.parent.name} -> {self.name} -> {self.children}"
        elif self.parent:
            return f"{self.parent.name} -> {self.name}"
        elif self.children:
            return f"{self.name} -> {self.children}"
        else:
            return f"{self.name}"


class Tree:
    def __init__(self):
        self.nodes = {}

    def add_relation(self, n1, n2):
        if n1 in self.nodes:
            n1 = self.nodes[n1]
        else:
            n1 = Node(n1)

        if n2 in self.nodes:
            n2 = self.nodes[n2]
        else:
            n2 = Node(n2)

        if n2.parent == None:
            n1.children.append(n2)
            n2.parent = n1
        else:
            print(f"{n1} already inserted")
            return

        self.nodes[n1.name] = n1
        self.nodes[n2.name] = n2

    def print(self):
        c = self.nodes["COM"]
        print(c.print())

    def count(self):
        x = 0
        for n in self.nodes.values():
            x += n._count()
        return x

def input_to_tree(input):
    input = input.split("\n")

    t = Tree()
    for l in input:
        l = l.strip()
        n1, n2 = l.split(")")
        t.add_relation(n1, n2)
    return t

def calculate_orbits(input):
    t = input_to_tree(input)
    return t.count()


def you_to_santa_path(t):
    you = t.nodes["YOU"].parents()
    san = t.nodes["SAN"].parents()
    you.reverse()
    san.reverse()
    print(f"you = {you}\nsan = {san}")
    intersection = [value for value in you if value in san]
    print(intersection)
    common = intersection[-1]
    result = you[you.index(common):] + san[san.index(common) + 1:]
    print(result)
    return len(result) - 1

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    t = input_to_tree(data)

    print(you_to_santa_path(t))
    print(t.count())


if __name__ == "__main__":
    main()
