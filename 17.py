WATER_LOCATION = [500, 0]
WATER_SOURCE = '+'
CLAY = '#'
SAND = '.'
FLOWING = '|'
SETTLED = '~'


def build_grid(data):
    for (i, line) in enumerate(data):
        line = line.split(', ')
        line = [coord.split('=') for coord in line]
        line[1] = [line[1][0], *line[1][1].split('..')]
        data[i] = line

    # determine extents
    xs = [int(line[0][1]) for line in data if line[0][0] == 'x']
    xs = xs + [int(line[1][2]) for line in data if line[1][0] == 'x']
    ys = [int(line[0][1]) for line in data if line[0][0] == 'y']
    ys = ys + [int(line[1][2]) for line in data if line[1][0] == 'y']
    max_x = max(xs)
    max_y = max(ys)

    grid = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]

    grid[WATER_LOCATION[1]][WATER_LOCATION[0]] = WATER_SOURCE

    for line in data:
        if line[0][0] == 'x':
            for y in range(int(line[1][1]), int(line[1][2]) + 1):
                grid[int(y)][int(line[0][1])] = CLAY
        else:
            for x in range(int(line[1][1]), int(line[1][2]) + 1):
                grid[int(line[0][1])][int(x)] = CLAY

    return grid


def p1(data):
    grid = build_grid(data)
    return grid


def p2(data):
    pass


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
