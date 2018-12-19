def p1_rec(data, total):
    if len(data) == 0:
        return total

    [num_children, num_metadata, *rest] = data
    if num_children == 0:
        metadata_sum = sum(rest[:num_metadata])
        rest = rest[num_metadata:]
        return (rest, total + metadata_sum)

    else:
        for _ in range(num_children):
            (rest, total) = p1_rec(rest, total)
        metadata_sum = sum(rest[:num_metadata])
        rest = rest[num_metadata:]
        return (rest, total + metadata_sum)


def p1(d):
    return p1_rec(d, 0)


def p2(data):
    [num_children, num_metadata, *rest] = data
    if num_children == 0:
        value = sum(rest[:num_metadata])
        rest = rest[num_metadata:]
        return (rest, value)

    else:
        child_values = []
        for _ in range(num_children):
            (rest, value) = p2(rest)
            child_values.append(value)
        metadata = rest[:num_metadata]
        value = 0
        for m in metadata:
            if (m - 1) < len(child_values):
                value += child_values[m - 1]
        rest = rest[num_metadata:]
        return (rest, value)


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [int(n) for n in f.read().strip().split()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
