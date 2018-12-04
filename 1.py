def p1(data):
    return sum([int(num) for num in data])


def p2(data):
    val = 0
    seen = set()
    seen.add(0)
    while True:
        for num in data:
            val += int(num)
            if val in seen:
                return val
            seen.add(val)


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
