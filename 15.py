from timeit import default_timer as timer

import pdb

WALL = '#'
OPEN = '.'
GOBLIN = 'G'
ELF = 'E'


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
    def __init__(self, raw):
        grid = []
        for (y, line) in enumerate(raw):
            grid.append([])
            for (x, char) in enumerate(line):
                if char == GOBLIN:
                    grid[y].append(Goblin(x, y))
                elif char == ELF:
                    grid[y].append(Elf(x, y))
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

    # def closest(self, location, location_set):
    #     # pdb.set_trace()
    #     distances = [{"location": l, "dist": manhattan_dist(
    #         location, l)} for l in location_set]
    #     distances.sort(key=lambda x: x["dist"])
    #     # pick top 5??
    #     return [d["location"] for d in distances[:5]]

    def build_distances(self, src, targets):
        print(src)
        # if src == [14, 8]:
        #     pdb.set_trace()
        src = str(src)
        vertices = [str(v) for v in self.get_open_squares()]
        vertices.append(src)
        distances = {v: float('inf') for v in vertices}
        prev = {v: [] for v in vertices}
        targets = [str(t) for t in targets]

        distances[src] = 0

        # pdb.set_trace()

        while len(vertices) > 0:
            current = min({k: v for (k, v) in distances.items()
                           if k in vertices}, key=distances.get)
            vertices.remove(current)

            if current in targets:
                continue

            # break if no targets in vertices
            if all([t not in vertices for t in targets]):
                break

            neighbours = [str(square)
                          for square in self.adjacent_squares(eval(current))]

            neighbours = [n for n in neighbours if n in vertices and
                          self.get_square_content(eval(n)) == OPEN]

            for v in neighbours:
                alt = distances[current] + 1
                if alt <= distances[v]:
                    distances[v] = alt
                    prev[v] = current  # .append(current)
                elif alt < distances[v]:
                    distances[v] = alt
                    prev[v] = current  # [current]

        # find closest target
        all_target_distances = {key: value for key,
                                value in distances.items() if key in targets}

        if len(all_target_distances.values()) == 0 or set(all_target_distances.values()) == set([float('inf')]):
            return None

        min_target_distance = min(all_target_distances.values())
        eligible_targets = [
            k for (k, v) in all_target_distances.items() if v == min_target_distance]

        the_target = str(first_in_reading_order(
            [eval(t) for t in eligible_targets]))

        # finding the first step on the path to that target
        # first_steps = self.build_first_steps(src, the_target, prev)
        # the_step = first_in_reading_order(
        # [eval(s) for s in [first_steps])

        # pdb.set_trace()
        possible_steps = self.get_open_adjacent_squares(eval(src))
        distances = [self.find_distance(step, the_target)
                     for step in possible_steps]
        min_distance = min(distances)
        possible_steps = [s[0] for s in zip(
            possible_steps, distances) if s[1] == min_distance]
        the_step = first_in_reading_order(possible_steps)

        # the_step = eval(self.build_first_steps(src, the_target, prev))
        # pdb.set_trace()
        return the_step

    def build_first_steps(self, src, target, prev_map):
        return self.build_first_steps_rec(src, target, prev_map, [])

    def build_first_steps_rec(self, src, current, prev_map, last_steps):
        if len(prev_map[current]) == 0 or current == src:
            return last_steps
        else:
            return self.build_first_steps_rec(src, prev_map[current], prev_map, current)

    def find_distance(self, src, target):
        src = str(src)
        vertices = [str(v) for v in self.get_open_squares()]
        vertices.append(src)
        distances = {v: float('inf') for v in vertices}
        target = str(target)

        distances[src] = 0

        while len(vertices) > 0:
            current = min({k: v for (k, v) in distances.items()
                           if k in vertices}, key=distances.get)
            vertices.remove(current)

            # if current == target:
            #     continue

            # break if no targets in vertices
            if target not in vertices:
                break

            neighbours = [str(square)
                          for square in self.adjacent_squares(eval(current))]

            neighbours = [n for n in neighbours if n in vertices and
                          self.get_square_content(eval(n)) == OPEN]

            for v in neighbours:
                alt = distances[current] + 1
                if alt <= distances[v]:
                    distances[v] = alt
                elif alt < distances[v]:
                    distances[v] = alt

        return distances[target]


# 1  S ← empty sequence
# 2  u ← target
# 3  if prev[u] is defined or u = source:          // Do something only if the vertex is reachable
# 4      while u is defined:                       // Construct the shortest path with a stack S
# 5          insert u at the beginning of S        // Push the vertex onto the stack
# 6          u ← prev[u]                           // Traverse from target to source

    # def find_distance(self, src, current, target, prev_map):
    #     if len(prev_map[current]) == 0 or current == src:
    #         return last_steps
    #     if len(prev_map[current]) == 1:
    #         return self.build_first_steps_rec(src, prev_map[current][0], prev_map, [current])
    #     else:

    # def build_first_steps(self, src, target, prev_map):
    #     return self.build_first_steps_rec(src, target, prev_map, [])

    # def build_first_steps_rec(self, src, current, prev_map, last_steps):
    #     if len(prev_map[current]) == 0 or current == src:
    #         return last_steps
    #     if len(prev_map[current]) == 1:
    #         return self.build_first_steps_rec(src, prev_map[current][0], prev_map, [current])
    #     else:
    #         last_steps = []
    #         for prev in prev_map[current]:
    #             last_steps = self.build_first_steps_rec(
    #                 src, prev, prev_map, current)
    #             for step in last_steps:
    #                 if step not in last_steps:
    #                     last_steps.append(step)
    #         return last_steps

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
                next_step = self.build_distances(
                    unit.location(), enemies_in_range)
                if next_step is not None and next_step != [float('inf'), float('inf')]:
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
            print('*******************')
            print(num_completed_rounds)
            print(self)
            print('*******************')
            for u in self.units():
                if self.game_over():
                    return num_completed_rounds * self.total_hitpoints()
                elif u.hp > 0:
                    if type(u) == Goblin:
                        self.turn(u, Elf)
                    else:
                        self.turn(u, Goblin)
            num_completed_rounds += 1


def p1(data):
    grid = Grid(data)
    print(grid)
    result = grid.run()
    print(grid)

    return result


def p2(data):
    pass


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
