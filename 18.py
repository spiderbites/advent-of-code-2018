import os

OPEN = '.'
TREES = '|'
LUMBERYARD = '#'


def safe_append(adjacent, grid, y, x):
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid):
        return
    adjacent.append(grid[y][x])


def tick(grid):
    new_grid = [row[:] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid)):
            adjacent = []
            safe_append(adjacent, grid, y-1, x-1)
            safe_append(adjacent, grid, y-1, x)
            safe_append(adjacent, grid, y-1, x+1)
            safe_append(adjacent, grid, y, x-1)
            safe_append(adjacent, grid, y, x+1)
            safe_append(adjacent, grid, y+1, x-1)
            safe_append(adjacent, grid, y+1, x)
            safe_append(adjacent, grid, y+1, x+1)

            if grid[y][x] == OPEN and sum(a == TREES for a in adjacent) >= 3:
                new_grid[y][x] = TREES
            elif grid[y][x] == TREES and sum(a == LUMBERYARD for a in adjacent) >= 3:
                new_grid[y][x] = LUMBERYARD
            elif grid[y][x] == LUMBERYARD and (sum(a == LUMBERYARD for a in adjacent) < 1 or sum(a == TREES for a in adjacent) < 1):
                new_grid[y][x] = OPEN
    return new_grid


def p1(grid):
    for _ in range(10):
        grid = tick(grid)
    return formula(grid)


def formula(grid):
    num_trees = sum(grid[y][x] == TREES for y in range(len(grid))
                    for x in range(len(grid[0])))
    num_lumberyards = sum(grid[y][x] == LUMBERYARD for y in range(len(grid))
                          for x in range(len(grid[0])))
    return num_trees * num_lumberyards


def p2(grid):
    grids = [grid]
    i = 0
    while True:
        i += 1
        grid = tick(grid)
        if grid in grids:
            break
        grids.append(grid)
    initial_index = grids.index(grid)

    cycle = i - initial_index
    print("cycle {0}, i {1}, initial match {2}".format(
        cycle, i, initial_index))

    loops_left = (1000000000 - i) % cycle

    print("loops left {0}".format(loops_left))

    for i in range(loops_left):
        grid = tick(grid)

    return formula(grid)


def print_grid(grid):
    for line in grid:
        print(''.join(line))


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [list(line.strip()) for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
