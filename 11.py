GRID_SIZE = 300


def build_grid(serial_number):
    grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            x += 1
            y += 1
            rack_id = x + 10
            power_level = rack_id * y
            power_level += serial_number
            power_level = power_level * rack_id
            power_level = (power_level // 100) % 10
            power_level -= 5
            x -= 1
            y -= 1
            grid[y][x] = power_level
    return grid


def p1(serial_number):
    grid = build_grid(serial_number)
    largest_power = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    for x in range(GRID_SIZE - 2):
        for y in range(GRID_SIZE - 2):
            total = 0
            for i in range(3):
                for j in range(3):
                    total += grid[y+i][x+j]
            largest_power[y][x] = total

    mx = -1
    mx_index = None
    for x in range(GRID_SIZE - 2):
        for y in range(GRID_SIZE - 2):
            if largest_power[y][x] > mx:
                mx = largest_power[y][x]
                mx_index = str(x + 1) + ',' + str(y + 1)
    return mx_index


def p2(serial_number):
    grid = build_grid(serial_number)

    # array of (x,y,z), where the z's contain the power level for the 1x1 ... NxN grids starting at (x,y)
    largest_power = [[[0 for z in range(GRID_SIZE)]
                      for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    for x in range(GRID_SIZE):
        print(x)
        for y in range(GRID_SIZE):
            # calculate every N x N grid where (x,y) is the top left corner
            for z in range(GRID_SIZE - max(x, y)):
                total = 0
                if z > 0:
                    # add the previous grid total
                    total += largest_power[y][x][z-1]
                # add the column to the right and the row to the bottom of the previous grid
                for i in range(z):
                    total += grid[y+i][x+z]
                    total += grid[y+z][x+i]
                # add the element at (N,N)
                total += grid[y+z][x+z]

                largest_power[y][x][z] = total

    mx = -1
    mx_index = None
    for x in range(GRID_SIZE - 2):
        for y in range(GRID_SIZE - 2):
            for z in range(GRID_SIZE - max(x, y)):
                if largest_power[y][x][z] > mx:
                    mx = largest_power[y][x][z]
                    mx_index = str(x + 1) + ',' + str(y + 1) + ',' + str(z + 1)
    return mx_index


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    # input = 18
    input = 5535
    answer = p1(input) if part == '1' else p2(input)
    print(answer)
