import copy
from collections import Counter
from functools import total_ordering

LEFT = '<'
UP = '^'
RIGHT = '>'
DOWN = 'v'

TURNS = [LEFT, DOWN, RIGHT, UP]
CARTS = [LEFT, DOWN, RIGHT, UP]

CURVE_R = '\\'
CURVE_L = '/'
INTERSECTION = '+'


@total_ordering
class Cart:
    def __init__(self, id, x, y, direction):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.turns = 0

    def turn(self):
        if self.turns % 3 == 0:
            self.direction = TURNS[(TURNS.index(self.direction) + 1) % 4]
        elif self.turns % 3 == 2:
            self.direction = TURNS[(TURNS.index(self.direction) - 1) % 4]
        else:
            pass
        self.turns += 1

    def location(self):
        return str(self.x) + ',' + str(self.y)

    def __str__(self):
        return "[{0}, {1}] {2}".format(self.x, self.y, self.direction)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


def find_carts(m):
    carts = []
    for (y, line) in enumerate(m):
        for (x, spot) in enumerate(line):
            if spot in CARTS:
                carts.append(Cart(len(carts), x, y, spot))
    return carts


def create_grid(m):
    for (i, line) in enumerate(m):
        m[i] = list(line)
    for (y, line) in enumerate(m):
        for (x, spot) in enumerate(line):
            if spot in CARTS:
                if spot == LEFT or spot == RIGHT:
                    m[y][x] = '-'
                elif spot == UP or spot == DOWN:
                    m[y][x] = '|'
    return m


def find_crash(carts):
    c = Counter([c.location() for c in carts])
    for (location, num_carts) in c.items():
        if num_carts > 1:
            return location
    return None


def move(c, grid):
    if c.direction == RIGHT:
        next_square = grid[c.y][c.x+1]
        c.x += 1
        if next_square == CURVE_R:
            c.direction = DOWN
        elif next_square == CURVE_L:
            c.direction = UP
        elif next_square == INTERSECTION:
            c.turn()
    elif c.direction == LEFT:
        next_square = grid[c.y][c.x-1]
        c.x -= 1
        if next_square == CURVE_R:
            c.direction = UP
        elif next_square == CURVE_L:
            c.direction = DOWN
        elif next_square == INTERSECTION:
            c.turn()
    elif c.direction == DOWN:
        next_square = grid[c.y+1][c.x]
        c.y += 1
        if next_square == CURVE_R:
            c.direction = RIGHT
        elif next_square == CURVE_L:
            c.direction = LEFT
        elif next_square == INTERSECTION:
            c.turn()
    elif c.direction == UP:
        next_square = grid[c.y-1][c.x]
        c.y -= 1
        if next_square == CURVE_R:
            c.direction = LEFT
        elif next_square == CURVE_L:
            c.direction = RIGHT
        elif next_square == INTERSECTION:
            c.turn()


def print_grid(carts, grid):
    g = copy.deepcopy(grid)
    for c in carts:
        g[c.y][c.x] = c.direction
    for row in g:
        print(''.join(row))
    print('*************')


def p1(data):
    carts = find_carts(data)
    grid = create_grid(data)
    while True:
        carts.sort()
        for cart in carts:
            move(cart, grid)
            crash = find_crash(carts)
            if crash is not None:
                return crash


def p2(data):
    carts = find_carts(data)
    grid = create_grid(data)
    i = 0
    carts.sort()
    while True:
        if i == len(carts):
            if len(carts) == 1:
                return carts[0].location()
            else:
                carts.sort()
                i = 0
        else:
            move(carts[i], grid)
            crash = find_crash(carts)
            if crash is not None:
                crashee_index = [j for j, c in enumerate(
                    carts) if c.location() == crash and j != i][0]
                carts = [c for c in carts if c.location() != crash]
                if crashee_index < i:
                    i -= 1
            else:
                i += 1


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.replace('\n', '') for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
