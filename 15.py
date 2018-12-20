from collections import deque
import math

WALL = '#'
OPEN = '.'
GOBLIN = 'G'
ELF = 'E'


def first_in_reading_order(locations):
    first = [float('inf'), float('inf')]
    for loc in locations:
        if loc[1] < first[1]:
            first = loc
        elif loc[1] == first[1]:
            if loc[0] < first[0]:
                first = loc
    return first


class Unit:
    def __init__(self, x, y, hp=200, ap=3):
        self.x = x
        self.y = y
        self.hp = hp
        self.ap = ap

    def location(self):
        return [self.x, self.y]


class Goblin(Unit):
    def __str__(self):
        return 'G'


class Elf(Unit):
    def __str__(self):
        return 'E'


class Grid:
    def __init__(self, raw, elf_ap=3):
        grid = []
        for (y, line) in enumerate(raw):
            grid.append([])
            for (x, char) in enumerate(line):
                if char == GOBLIN:
                    grid[y].append(Goblin(x, y))
                elif char == ELF:
                    grid[y].append(Elf(x, y, 200, elf_ap))
                else:
                    grid[y].append(char)
        self.grid = grid

    def __str__(self):
        rep = ''
        for line in self.grid:
            rep += "".join([str(c) for c in line]) + '\n'
        return rep

    def get_square_content(self, location):
        [x, y] = location
        return self.grid[y][x]

    def get_open_squares(self):
        s = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] == OPEN:
                    s.append([x, y])
        return s

    def units(self):
        units = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if isinstance(self.grid[y][x], Unit):
                    units.append(self.grid[y][x])
        return units

    def all_of_type(self, t):
        units = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if type(self.grid[y][x]) == t:
                    units.append(self.grid[y][x])
        return units

    def goblins(self):
        return self.all_of_type(Goblin)

    def elves(self):
        return self.all_of_type(Elf)

    def game_over(self):
        return len(self.goblins()) == 0 or len(self.elves()) == 0

    def total_hitpoints(self):
        return sum([u.hp for u in self.units()])

    def adjacent_squares(self, location):
        [x, y] = location
        return [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]

    def get_open_adjacent_squares(self, location):
        adjacent = self.adjacent_squares(location)
        return [[x, y] for [x, y] in adjacent if self.grid[y][x] == OPEN]

    def adjacent_enemies(self, location, enemy_type):
        adjacent = self.adjacent_squares(location)
        square_contents = [self.get_square_content(a) for a in adjacent]
        return [c for c in square_contents if type(c) == enemy_type]

    def enemies_in_range(self, enemy_type):
        all_enemies = self.all_of_type(enemy_type)
        adjacent = [self.get_open_adjacent_squares(
            e.location()) for e in all_enemies]
        flattened = [item for sublist in adjacent for item in sublist]
        unique = []
        for item in flattened:
            if item not in unique:
                unique.append(item)
        return unique

    def bfs(self, src, targets):
        root = str(src)
        targets = [str(t) for t in targets]

        open_set = deque()  # unvisited nodes
        closed_set = set()  # visited nodes
        meta = dict()  # for storing every nodes parent

        meta[root] = None
        open_set.append(root)

        while not len(open_set) == 0:
            current = open_set.popleft()

            neighbours = [n for n in self.get_open_adjacent_squares(
                eval(current)) if str(n) not in closed_set]

            for n in neighbours:
                n = str(n)
                if n not in open_set:
                    meta[n] = current
                    open_set.append(n)

            closed_set.add(current)

        # construct the paths to each target
        paths = []
        for t in targets:
            if t not in meta:
                continue
            path = [t]
            while meta[t] is not None:
                parent = meta[t]
                path.append(parent)
                t = parent
            path.reverse()
            paths.append(path)

        if len(paths) == 0:
            return None

        # find the best target
        min_length = min(len(path) for path in paths)
        eligible_targets = [p[-1] for p in paths if len(p) == min_length]
        the_target = first_in_reading_order(
            [eval(t) for t in eligible_targets])

        return str(the_target)

    def find_the_step(self, src, targets):
        the_target = self.bfs(src, targets)

        possible_steps = [str(s)
                          for s in self.get_open_adjacent_squares(src)]

        if the_target is None:
            return None

        the_step = self.bfs(the_target, possible_steps)

        return eval(the_step)

    def attack(self, attacker, attackee):
        attackee.hp = attackee.hp - attacker.ap

    def choose_weakest_enemy(self, enemies):
        weakest = Unit(0, 0, float('inf'))
        for e in enemies:
            if e.hp < weakest.hp:
                weakest = e
            # reading order...
            elif e.hp == weakest.hp:
                if e.y < weakest.y:
                    weakest = e
                elif e.y == weakest.y:
                    if e.x < weakest.x:
                        weakest = e
        return weakest

    def turn(self, unit, enemy_type):
        enemies = self.adjacent_enemies(unit.location(), enemy_type)

        # move
        if len(enemies) == 0:
            enemies_in_range = self.enemies_in_range(enemy_type)
            if len(enemies_in_range) > 0:
                next_step = self.find_the_step(
                    unit.location(), enemies_in_range)

                if next_step is not None:
                    [cur_x, cur_y] = unit.location()
                    [new_x, new_y] = next_step

                    unit.x = new_x
                    unit.y = new_y

                    self.grid[new_y][new_x] = unit
                    self.grid[cur_y][cur_x] = OPEN

        enemies = self.adjacent_enemies(unit.location(), enemy_type)

        # attack
        if len(enemies) > 0:
            weakest_enemy = self.choose_weakest_enemy(enemies)
            self.attack(unit, weakest_enemy)
            if weakest_enemy.hp <= 0:
                [x, y] = weakest_enemy.location()
                self.grid[y][x] = OPEN

    def run_round(self):
        for u in self.units():
            if type(u) == Goblin:
                self.turn(u, Elf)
            else:
                self.turn(u, Goblin)

    def run(self):
        num_completed_rounds = 0
        while True:
            print(num_completed_rounds, end=" ", flush=True)
            for u in self.units():
                if self.game_over():
                    return num_completed_rounds * self.total_hitpoints()
                elif u.hp > 0:
                    if type(u) == Goblin:
                        self.turn(u, Elf)
                    else:
                        self.turn(u, Goblin)
            num_completed_rounds += 1
        print('\n')


def p1(data):
    grid = Grid(data)
    result = grid.run()
    return result


def p2(data):
    grid = Grid(data, 1000)
    total_elves = len(grid.elves())

    # implementing a binary search to find the minimum ap for which all elves survive
    min_attack_power = 4
    max_attack_power = 1000  # decided on this number empirically
    aps = [min_attack_power, max_attack_power]

    while True:
        cur_ap = math.floor(
            (aps[1] + aps[0]) / 2)
        print("\nElf attack power: {0}".format(cur_ap))
        grid = Grid(data, cur_ap)
        result = grid.run()

        if len(grid.elves()) != total_elves:
            # At least one elf died...
            if aps[0] - aps[1] == 0:
                # corner case, ap is too low between bounds are equal
                aps = [cur_ap + 1, cur_ap + 1]
            else:
                # set bottom ap bound to midpoint + 1
                aps[0] = cur_ap + 1
        else:
            # no dead elves!
            if aps[1] - aps[0] <= 1:
                # we've found the minimum ap for which this occurs
                return result
            else:
                # set top ap bound to midpoint - 1
                aps[1] = cur_ap - 1
    return result


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
