import re

MATCH_NEW_STACK = re.compile(".*new.stack.*")
MATCH_CUT = re.compile("cut.(?P<n>[-0-9]+)")
MATCH_INCREMENT = re.compile(".*increment.(?P<n>[-0-9]+)")

def new_deck(n):
    return [i for i in range(n)]

def new_stack(deck):
    deck.reverse()
    return deck

def cut(deck, n):
    return deck[n:] + deck[:n]

def increment(deck, n):
    l = len(deck)
    nd = [None for i in range(l)]
    for i, v in enumerate(deck):
        nd[(l + i * n) % l] = v
    return nd

def slam_shuffle(input, deck_size):
    input = input.strip()
    deck = new_deck(deck_size)

    scale = 1
    shift = 0

    for l in input.split("\n"):
        print(f"==> {l}")
        m = MATCH_NEW_STACK.match(l)
        if m:
            print(f"new_stack")
            scale *= -1
            shift *= -1
            shift -= 1
            deck = new_stack(deck)
            #print(f"after new_stack {deck}")
        m = MATCH_CUT.match(l)
        if m:
            v = int(m.groups('n')[0])
            shift -= v
            print(f"cut {v}")
            deck = cut(deck, v)
            #print(f"after cut {deck}")
        m = MATCH_INCREMENT.match(l)
        if m:
            v = int(m.groups('n')[0])
            scale *= v
            shift *= v
            print(f"increment {v}")
            deck = increment(deck, v)
            #print(f"after increment {deck}")
        # print(deck)
    return deck, (scale, shift)

def apply(n, mod, chg):
    n *= chg[0]
    n += chg[1]
    return n % mod

def main():
    with open("input.txt", "r") as f:
        data = f.read()
        data = data.strip()

        deck, chg = slam_shuffle(data, 10007)
        print(deck)
        print(deck[2010:2030])
        print(apply(2019, 10007, chg))

    giant_deck = 119315717514047
    shuffle_times = 101741582076661

    print()

if __name__ == "__main__":
    main()