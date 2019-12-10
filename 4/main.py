
def is_valid_password(i):
    p = str(i)
    if len(p) != 6:
        return False

    last_digit = None
    for i, digit in enumerate(p):
        d = int(digit, 10)
        if not last_digit:
            last_digit = d
            continue

        if d < last_digit:
            return False

        last_digit = d

    for i, digit in enumerate(p):
        c = p.count(digit)
        if c == 2:
            return True

    return False


passwd_ctn = 0
for i in range(357253, 892942):
    if is_valid_password(i):
        passwd_ctn += 1

print(passwd_ctn)