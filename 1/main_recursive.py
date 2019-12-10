
from math import floor


def calculate_fuel(mass):
    fuel = floor(mass / 3.0) - 2
    return fuel


def fuel_required(mass):
    fuel = 0
    partial_fuel = calculate_fuel(mass)
    print(partial_fuel)
    fuel += partial_fuel
    while partial_fuel >= 0:
        partial_fuel = calculate_fuel(partial_fuel)
        if partial_fuel >= 0:
            fuel += partial_fuel
    return fuel


fuel_values = []

with open("input.txt", "r") as f:
    data = f.readlines()
    for l in data:
        fuel = fuel_required(int(l.strip(), 10))
        fuel_values.append(fuel)

print(sum(fuel_values))
