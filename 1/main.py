
from math import floor

def fuel_required(mass):
    fuel = floor(mass / 3.0) - 2
    return fuel

fuel_values  = []

with open("input.txt", "r") as f:
    data = f.readlines()
    for l in data:
        fuel_values.append(fuel_required(int(l.strip(), 10)))

print(sum(fuel_values))


