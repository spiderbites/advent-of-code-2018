import pdb

ROCKY = '.'
WET = '='
NARROW = '|'


def erosion_level(geo_index, cave_depth):
    return (geo_index + cave_depth) % 20183


def region_type(erosion_level):
    switch = {
        0: ROCKY,
        1: WET,
        2: NARROW
    }
    return switch[erosion_level % 3]


def process_square(x, y, grid, depth, target):
    [targetx, targety] = target
    if x == targetx and y == targety:
        grid[y][x]["g"] = 0
    elif x == 0 and y == 0:
        grid[y][x]["g"] = 0
    elif x == 0:
        grid[y][x]["g"] = y * 48271
    elif y == 0:
        grid[y][x]["g"] = x * 16807
    else:
        grid[y][x]["g"] = grid[y][x-1]["e"] * grid[y-1][x]["e"]
    grid[y][x]["e"] = erosion_level(grid[y][x]["g"], depth)
    grid[y][x]["t"] = region_type(grid[y][x]["e"])


def build_map(depth, target):
    [x, y] = target
    extra_x = 10
    extra_y = 10
    grid = [[None] * (x + extra_x + 1) for i in range(y + extra_y + 1)]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x] = {"e": None, "g": None, "t": None}
            process_square(x, y, grid, depth, target)
    return grid


def print_grid(g):
    for line in g:
        print(''.join(c["t"] for c in line))


def risk_level(grid, target):
    [targetx, targety] = target
    switch = {
        ROCKY: 0,
        WET: 1,
        NARROW: 2
    }
    return sum([switch[grid[y][x]["t"]] for y in range(targety + 1) for x in range(targetx + 1)])


def p1(depth, target):
    grid = build_map(depth, target)
    print_grid(grid)
    return risk_level(grid, target)


def p2(data):
    pass


if __name__ == "__main__":
    import sys
    [part, _] = sys.argv[1:]
    # answer = p1(data) if part == '1' else p2(data)
    # print(answer)
    # test values
    # depth = 510
    # target = [10, 10]
    depth = 10647
    target = [7, 770]
    if part == '1':
        answer = p1(depth, target)
    print(answer)
