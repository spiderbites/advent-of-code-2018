def has_repetition(word, num):
    counts = {}
    for w in word:
        counts[w] = counts[w] + 1 if w in counts else 1
    return num in counts.values()


def p1(words):
    has_two = sum(map(lambda x: has_repetition(x, 2), words))
    has_three = sum(map(lambda x: has_repetition(x, 3), words))
    return has_two * has_three


def p2(words):
    for w1 in words:
        for w2 in words:
            if diff_count(w1, w2) == 1:
                return common(w1, w2)


def diff_count(w1, w2):
    return sum(map(lambda x: x[0] != x[1], list(zip(w1, w2))))


def common(w1, w2):
    cmn = filter(lambda x: x[0] == x[1], list(zip(w1, w2)))
    return "".join(map(lambda x: x[0], cmn))


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
