import string


def p1_rec(s):
    # maximum depth exceeded
    for i in range(len(s)-1):
        if abs(ord(s[i]) - ord(s[i+1])) == 32:
            return p1(s[0:i] + s[i+2:])
    return len(s)


def p1(s):
    i = 0
    while (i < len(s)-1):
        if abs(ord(s[i]) - ord(s[i+1])) == 32:
            s = s[0:i] + s[i+2:]
            i = max(i - 1, 0)
        else:
            i += 1
    return len(s)


def p2(s):
    m = float("inf")
    for l in string.ascii_lowercase:
        table = str.maketrans(dict.fromkeys(l + chr(ord(l) - 32)))
        m = min(m, p1(s.translate(table)))
    return m


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = f.read().strip()
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
