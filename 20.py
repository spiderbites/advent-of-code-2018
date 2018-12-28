from collections import deque
import re
from collections import Counter
import pdb

DIRECTIONS = ['N', 'S', 'E', 'W']


class Node:
    def __init__(self, x, y):
        self.id = "{0},{1}".format(x, y)
        self.x = x
        self.y = y
        self.neighbours = []

    def __str__(self):
        return self.id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes

    def bfs(self):
        root = next(n for n in self.nodes if n.x == 0 and n.y == 0)
        open_set = deque()
        closed_set = set()
        distances = dict()

        distances[root.id] = 0

        open_set.append(root)

        while not len(open_set) == 0:
            current = open_set.popleft()

            for n in [node for node in current.neighbours if node.id not in closed_set]:
                distances[n.id] = distances[current.id] + 1
                if n not in open_set:
                    open_set.append(n)

            closed_set.add(current.id)

        return distances


def get_direction(x, y, step):
    if step == 'N':
        return (x, y+1)
    if step == 'E':
        return (x+1, y)
    if step == 'W':
        return (x-1, y)
    if step == 'S':
        return (x, y-1)


def build_graph(input):
    q = deque()
    head = Node(0, 0)
    nodes = {}
    nodes[head.id] = head

    for char in input:
        if char == '(':
            q.append(head)
        elif char == '|':
            head = q[-1]
        elif char == ')':
            q.pop()
        else:
            (x, y) = get_direction(head.x, head.y, char)
            newhead = Node(x, y)
            nodes[newhead.id] = newhead
            head.neighbours.append(newhead)
            head = newhead

    return nodes


def p1(input):
    input = input[1:-1]

    nodes = build_graph(input)

    graph = Graph(list(nodes.values()))
    distances = graph.bfs()

    return max(d for d in distances.values())


def p2(input):
    input = input[1:-1]

    nodes = build_graph(input)

    graph = Graph(list(nodes.values()))
    distances = graph.bfs()

    return len([d for d in distances.values() if d >= 1000])


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = f.read().strip()
    answer = p1(data) if part == '1' else p2(data)
    print(answer)

    # p1 tests
    # assert p1('^WNE$') == 3
    # assert p1('^ENWWW(NEEE|SSE(EE|N))$') == 10, p1('^ENWWW(NEEE|SSE(EE|N))$')
    # assert p1('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$') == 18, p1(
    #     '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    # assert p1('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$') == 23
    # assert p1(
    #     '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$') == 31
