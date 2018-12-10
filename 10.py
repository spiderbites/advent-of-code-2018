import time
import re


def read(d):
    # position=< 9,  1> velocity=< 0,  2>
    lines = [re.findall(r'position=<(.*)> velocity=<(.*)>', line)[0]
             for line in d]

    return [Point(l) for l in lines]


class Point:
    def __init__(self, data):
        position = [int(p) for p in data[0].strip().split(', ')]
        velocity = [int(p) for p in data[1].strip().split(', ')]
        self.position = position
        self.velocity = velocity

    def tick(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


def extents(points):
    ys = [p.position[1] for p in points]
    xs = [p.position[0] for p in points]
    min_y, max_y = min(ys), max(ys)
    min_x, max_x = min(xs), max(xs)
    return (min_y, max_y, min_x, max_x)


def run(points):
    seconds = 0
    last_diff = float('inf')

    while True:
        (min_y, max_y, min_x, max_x) = extents(points)

        # get rid of negative values
        for p in points:
            p.position[0] - min_x
            p.position[1] - min_y

        # get new extents
        (min_y, max_y, min_x, max_x) = extents(points)

        print("size {0} x {1}".format(max_x - min_x, max_y - min_y))

        # arrived at empirically, only print if grid size is small, otherwise, probably just noise
        diff = max_x - min_x
        if (diff < 75):
            grid = [['.' for j in range(min_x, max_x + 1)]
                    for i in range(min_y, max_y + 1)]
            for p in points:
                y = p.position[1] - min_y
                x = p.position[0] - min_x
                grid[y][x] = '#'
            for line in grid:
                print(''.join(line))
            print("seconds {0}".format(seconds))
            time.sleep(1)
        for p in points:
            p.tick()
        seconds += 1
        if diff > last_diff:
            break
        last_diff = diff


def p1(d):
    points = read(d)
    run(points)


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    p1(data)
