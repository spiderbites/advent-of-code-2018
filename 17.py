import pdb

WATER_LOCATION = [500, 0]
WATER_SOURCE = '+'
CLAY = '#'
SAND = '.'
FLOWING = '|'
SETTLED = '~'


class Cursor:
    def __init__(self, src):
        self.x = src[0]
        self.y = src[1]


def build_grid(data):
    for (i, line) in enumerate(data):
        line = line.split(', ')
        line = [coord.split('=') for coord in line]
        line[1] = [line[1][0], *line[1][1].split('..')]
        data[i] = line

    # determine extents
    xs = [int(line[0][1]) for line in data if line[0][0] == 'x']
    xs = xs + [int(line[1][1]) for line in data if line[1][0] == 'x']
    xs = xs + [int(line[1][2]) for line in data if line[1][0] == 'x']
    ys = [int(line[0][1]) for line in data if line[0][0] == 'y']
    ys = ys + [int(line[1][1]) for line in data if line[1][0] == 'y']
    ys = ys + [int(line[1][2]) for line in data if line[1][0] == 'y']

    max_x = max(xs)
    max_y = max(ys)
    min_y = min(ys)

    grid = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]

    grid[WATER_LOCATION[1]][WATER_LOCATION[0]] = WATER_SOURCE

    for line in data:
        if line[0][0] == 'x':
            for y in range(int(line[1][1]), int(line[1][2]) + 1):
                grid[int(y)][int(line[0][1])] = CLAY
        else:
            for x in range(int(line[1][1]), int(line[1][2]) + 1):
                grid[int(line[0][1])][int(x)] = CLAY

    return (grid, min_y)


def flow_down(cursor, grid):

    next_flows = []

    # flow down
    if grid[cursor.y + 1][cursor.x] == SAND:
        while cursor.y + 1 < len(grid) and grid[cursor.y + 1][cursor.x] == SAND:
            cursor.y += 1
            grid[cursor.y][cursor.x] = FLOWING

    # flowed off bottom
    if cursor.y + 1 == len(grid):
        return []

    # flowed into already flowing water
    if grid[cursor.y + 1][cursor.x] in [FLOWING]:
        return []

    # on some clay, fill left and right and then move up
    full = False
    while not full:
        # find the furthest points left and right
        min_x, max_x = cursor.x, cursor.x
        while grid[cursor.y][min_x - 1] != CLAY and grid[cursor.y+1][min_x - 1] in [SETTLED, CLAY]:
            min_x -= 1
        while grid[cursor.y][max_x + 1] != CLAY and grid[cursor.y+1][max_x + 1] in [SETTLED, CLAY]:
            max_x += 1

        # if min_x and max_x are both above settled water or clay, this water will settle
        if grid[cursor.y + 1][min_x - 1] in [SETTLED, CLAY] and grid[cursor.y + 1][max_x + 1] in [SETTLED, CLAY]:
            for x in range(min_x, max_x + 1):
                grid[cursor.y][x] = SETTLED
            # move back up
            cursor.y -= 1

        # this water will overflow
        else:
            # water will overflow to the left
            if grid[cursor.y + 1][min_x - 1] not in [SETTLED, CLAY]:
                for x in range(min_x - 1, max_x + 1):
                    grid[cursor.y][x] = FLOWING
                next_flows.append(Cursor([min_x - 1, cursor.y]))

            # water will overflow to the right
            if grid[cursor.y + 1][max_x + 1] not in [SETTLED, CLAY]:
                for x in range(min_x, max_x + 2):
                    grid[cursor.y][x] = FLOWING
                next_flows.append(Cursor([max_x + 1, cursor.y]))

            full = True

    return next_flows


def run_water(grid):
    next_flows = [Cursor(WATER_LOCATION)]
    rounds = 0
    while len(next_flows) > 0:
        next_flows = [flow_down(f, grid) for f in next_flows]
        next_flows = flatten(next_flows)
        rounds += 1
    return grid


def flatten(l):
    return [item for sublist in l for item in sublist]


def print_grid(grid):
    for line in grid:
        print(''.join(line[-275:]))


def p1(data):
    (grid, min_y) = build_grid(data)
    grid = run_water(grid)
    return sum([grid[y][x] in [SETTLED, FLOWING] for y in range(min_y, len(grid)) for x in range(len(grid[0]))])


def p2(data):
    (grid, min_y) = build_grid(data)
    grid = run_water(grid)
    return sum([grid[y][x] == SETTLED for y in range(min_y, len(grid)) for x in range(len(grid[0]))])


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
