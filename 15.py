import pdb

WALL = '#'
OPEN = '.'
GOBLIN = 'G'
ELF = 'E'


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

    # def open_square_adjacent(self, square):
    #     adjacent = self.adjacent_squares(square)
    #     return any([self.grid[y][x] == OPEN for [x, y] in adjacent])

    # def all_in_range(self, t):
    #     return [unit for unit in self.all_of_type(t) if self.open_square_adjacent(unit.location())]

    def adjacent_enemies(self, location, enemy_type):
        adjacent = self.adjacent_squares(location)
        square_contents = [self.get_square_content(a) for a in adjacent]
        return [c for c in square_contents if type(c) == enemy_type]

    def enemies_in_range(self, enemy_type):
        all_enemies = self.all_of_type(enemy_type)
        adjacent = [self.get_open_adjacent_squares(
            e.location()) for e in all_enemies]
        # flatten
        return [item for sublist in adjacent for item in sublist]

    def find_distance(self, a, b):
        return self.__find_distance_rec(a, b, 0, [])

    def __find_distance_rec(self, current, target, d, path):

        # def shortest_distance_cmp(d1, d2):
        #     (distance1, path1) = d1, (distance2, path2) = d2
        #     if distance1 < distance2:
        #         return distance1
        #     return path1[0] < path2[0]

        if current == target:
            return (d, path)
        else:
            options = self.adjacent_squares(current)
            valid_options = [o for o in options if (self.grid[o[1]]
                                                    [o[0]] == OPEN or o == target) and o not in path]

            if valid_options == []:
                return (float('inf'), None)

            return min([self.__find_distance_rec(o, target, d + 1, path + [o]) for o in valid_options])

    def attack(self, attacker, attackee):
        attackee.hp = attackee.hp - attacker.ap

    def choose_step(self, possible_moves):
        best = (float('inf'), [[0, 0]])
        for m in possible_moves:
            (distance, path) = m
            if distance < best[0]:
                best = m
            # reading order...
            elif distance == best[0]:
                [best_x, best_y] = best[1][0]
                [path_x, path_y] = path[0]
                if path_y < best_y:
                    best = m
                elif path_y == best_y:
                    if path_x < best_x:
                        best = m
        return best[1][0]

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
        # pdb.set_trace()
        enemies = self.adjacent_enemies(unit.location(), enemy_type)

        # move
        if len(enemies) == 0:
            enemies_in_range = self.enemies_in_range(enemy_type)

            all_moves = [self.find_distance(
                unit.location(), square) for square in enemies_in_range]

            possible_moves = [
                move for move in all_moves if move != (float('inf'), None)]

            if len(possible_moves) > 0:
                next_step = self.choose_step(possible_moves)

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
            # print([(isinstance(u, Elf), u.hp) for u in self.units()])
            for u in self.units():
                if self.game_over():
                    return num_completed_rounds * self.total_hitpoints()
                elif type(u) == Goblin:
                    # pdb.set_trace()
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
    f = open('./inputs/15_test_6.txt', 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
