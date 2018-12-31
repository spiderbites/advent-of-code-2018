import time
from functools import total_ordering
import heapq
import pdb

ROCKY = '.'
WET = '='
NARROW = '|'

CLIMBING_GEAR = 'CG'
TORCH = 'T'
NEITHER = 'N'

TOOL_SWITCH_COST = 7
STEP_COST = 1

TOOL_FOR_REGION_TYPE = {
    ROCKY: [CLIMBING_GEAR, TORCH],
    WET: [CLIMBING_GEAR, NEITHER],
    NARROW: [TORCH, NEITHER]
}


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
    extra_x = 50
    extra_y = 50
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


def neighbouring_squares(x, y, max_x, max_y):
    all_neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    valid_neighbours = [(x, y) for (
        x, y) in all_neighbours if 0 <= x < max_x and 0 <= y < max_y]
    return valid_neighbours


def build_graph(map):
    g = Graph()

    # add nodes
    for y in range(len(map)):
        for x in range(len(map[0])):
            cur_region_type = map[y][x]["t"]
            for t in TOOL_FOR_REGION_TYPE[cur_region_type]:
                g.add_node(Node(x, y, cur_region_type, t))

    for n in g.nodes:
        # add edge from this tool to other tools
        for t in TOOL_FOR_REGION_TYPE[n.region_type]:
            if n.tool != t:
                g.add_edge(n, Node(n.x, n.y, n.region_type, t),
                           TOOL_SWITCH_COST)

        # add edge from this location to neighbouring locations with this tool
        # (if this tool can be used in that location)
        neighbours = neighbouring_squares(n.x, n.y, len(map[0]), len(map))
        for neighbour in neighbours:
            (neighbour_x, neighbour_y) = neighbour
            neighbour_node = Node(neighbour_x, neighbour_y,
                                  map[neighbour_y][neighbour_x]["t"], n.tool)
            if n.tool in TOOL_FOR_REGION_TYPE[neighbour_node.region_type]:
                g.add_edge(n, neighbour_node, 1)

    return g


@total_ordering
class Node:
    def __init__(self, x, y, region_type, tool):
        self.id = "{0},{1} ({2}) ({3})".format(x, y, region_type, tool)
        self.x = x
        self.y = y
        self.region_type = region_type
        self.tool = tool
        self.distance = 0

    def __str__(self):
        return self.id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.tool == other.tool

    def __lt__(self, other):
        return self.distance < other.distance


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, frm, to, cost):
        if frm.id not in self.edges:
            self.edges[frm.id] = []
        self.edges[frm.id].append({
            "to": to.id,
            "cost": cost
        })

    def dijkstra(self, start_id, target_id):
        q = self.nodes[:]
        heapq.heapify(q)

        nodes_by_id = {node.id: node for node in q}
        nodes_in_q = {node.id: None for node in q}

        root = nodes_by_id[start_id]
        root.distance = 0

        for n in self.nodes:
            if n != root:
                n.distance = float('inf')

        q.sort()

        while len(q) != 0:
            # print(len(q))
            current = heapq.heappop(q)
            nodes_in_q.pop(current.id)
            edges = [e for e in self.edges[current.id]
                     if e["to"] in nodes_in_q]
            for e in edges:
                v = nodes_by_id[e["to"]]
                alt = current.distance + e['cost']
                if alt < v.distance:
                    v.distance = alt
            q.sort()

            if current.id == target_id:
                break

        return nodes_by_id[target_id].distance


def p1(depth, target):
    grid = build_map(depth, target)
    print_grid(grid)
    return risk_level(grid, target)


def p2(depth, target):
    grid = build_map(depth, target)
    graph = build_graph(grid)

    start_id = '0,0 (.) (T)'

    [target_x, target_y] = target
    target_region_type = grid[target_y][target_x]["t"]
    target_tool = TORCH
    target = Node(target_x, target_y, target_region_type, target_tool)
    return graph.dijkstra(start_id, target.id)


if __name__ == "__main__":
    import sys
    [part, _] = sys.argv[1:]
    # test values
    # depth = 510
    # target = [10, 10]
    depth = 10647
    target = [7, 770]
    if part == '1':
        answer = p1(depth, target)
    elif part == '2':
        answer = p2(depth, target)
    print(answer)
