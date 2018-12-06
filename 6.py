from collections import Counter
import string


def p1(d):
    min_x = min([i[0] for i in d])
    max_x = max([i[0] for i in d])
    min_y = min([i[1] for i in d])
    max_y = max([i[1] for i in d])

    grid = [['.'] * (max_x + 1) for i in range(max_y + 1)]
    ltrs = string.ascii_lowercase + string.ascii_uppercase

    infinites = []

    near = [0] * len(d)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = [dist([x, y], coord) for coord in d]
            closest = distances.index(min(distances))
            if Counter(distances)[min(distances)] == 1:
                near[closest] += 1
                grid[y][x] = ltrs[closest]
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinites.append(closest)

    for i in infinites:
        near[i] = 0

    # print_grid(grid)
    return max(near)


def print_grid(g):
    for line in g:
        for i in line:
            print(i, end="")
        print()


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def p2(d):
    min_x = min([i[0] for i in d])
    max_x = max([i[0] for i in d])
    min_y = min([i[1] for i in d])
    max_y = max([i[1] for i in d])

    size = 0

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = [dist([x, y], coord) for coord in d]
            total = sum(distances)
            if total < 10000:
                size += 1

    return size


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [list(map(int, line.strip().split(', '))) for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
