import re
import math

MATCH_AMOUNT_NAME = re.compile(r"(?P<amount>\d+).(?P<name>\w+)")
sign = lambda x: x and (-1 if x < 0 else 1)


class Equation:
    def __init__(self, name, amount, inputs):
        self.name = name
        self.amount = amount
        self.inputs = inputs

    def __str__(self):
        return f"<Equation: {self.name} {self.amount} inputs:({self.inputs})>"


def create_equation(line):
    products, output = line.split("=>")
    output = output.strip()
    m = MATCH_AMOUNT_NAME.match(output)
    name = str(m["name"])
    amount = int(m["amount"])

    inputs = []
    for p in products.split(","):
        p = p.strip()
        m = MATCH_AMOUNT_NAME.match(p)
        inputs.append((str(m["name"]), int(m["amount"])))

    return Equation(name, amount, inputs)

def process_input(input):
    data = {}
    for l in input.split("\n"):
        eq = create_equation(l.strip())
        data[eq.name] = eq
    return data


def calculate_recursive(equations, cur, amount, inventory):
    # print(cur, amount, inventory)
    if cur == "ORE":
        return amount

    in_stock = inventory.get(cur, 0)
    if in_stock > 0:
        x = in_stock - amount
        inventory[cur] = x if x >= 0 else 0
        needed = amount - in_stock
    else:
        needed = amount

    if needed <= 0:
        # print(0)
        return 0

    required = int(math.ceil( needed / equations.get(cur).amount ))
    produced = equations.get(cur).amount * required
    print(f"{cur} required: {required} produced: {produced} amount: {amount} needed: {needed}")
    if needed < produced:
        inventory[cur] = inventory.get(cur, 0) + produced - needed

    total = 0
    inputs = equations.get(cur)
    for component in inputs.inputs:
        p = calculate_recursive(equations, component[0], component[1] * required, inventory)
        total += p

    return total



def calculate_needed_ore(equations):
    eq = equations["FUEL"]
    inventory = {}
    amount = calculate_recursive(equations, eq.name, eq.amount, inventory)
    return amount

def find_maximum_fuel_with_trillion_ore(equations):
    max_ore = 1000000000000
    low = step = max_ore // calculate_needed_ore(equations)
    #low = 0
    i = 0
    high = max_ore
    step = 1
    r = 0
    while low < high:
        if i == 0:
            step = low
        else:
            step = (high + low) // 2
        i += 1
        print(low, high, step)
        inventory = {}
        r = calculate_recursive(equations, "FUEL", step, inventory)
        print(r, step)
        if r > max_ore:
            high = step - 1
        elif r < max_ore:
            low = step + 1
        elif r == max_ore:
            return step
    print(i)
    return low


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    input = process_input(data)
    for i in input:
        print(input[i])
    r = calculate_needed_ore(input)
    print(r)


def main2():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()
    input = process_input(data)
    for i in input:
        print(input[i])
    r = find_maximum_fuel_with_trillion_ore(input)
    print(r)

if __name__ == "__main__":
    main2()