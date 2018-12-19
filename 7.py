import re
from functools import total_ordering

NUM_WORKERS = 5


@total_ordering
class Node:
    def __init__(self, name):
        self.name = name
        self.prev = []
        self.nxt = []
        self.done = False
        self.time = (ord(name) - 64) + 60

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.name, self.prev, self.nxt, self.done, self.time)

    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __lt__(self, other):
        return self.name < other.name


class Worker:
    def __init__(self):
        self.node = None
        self.time_worked = None

    def assign(self, n):
        self.node = n
        self.time_worked = 0

    def work(self):
        self.time_worked += 1

    def done(self):
        self.node = None
        self.time_worked = 0


def parse_steps(lines):
    return [re.findall(r'Step (\w).*step (\w).*', line)[0] for line in lines]


def build_nodes(steps):
    nodes = {}
    for (a, b) in steps:
        if a not in nodes:
            nodes[a] = Node(a)
        if b not in nodes:
            nodes[b] = Node(b)
    for (a, b) in steps:
        nodes[a].nxt.append(nodes[b])
        nodes[b].prev.append(nodes[a])
    return list(nodes.values())


def p1(d):
    steps = parse_steps(d)
    nodes = build_nodes(steps)

    n = find_next_p1(nodes)
    result = ''
    while n is not None:
        result += n.name
        n.done = True
        n = find_next_p1(nodes)
    return result


def find_next_p1(nodes):
    ready = []
    for node in nodes:
        if node.done:
            continue
        elif len(node.prev) == 0:
            ready.append(node)
        else:
            if all(n.done for n in node.prev):
                ready.append(node)
    if len(ready) > 0:
        return min(ready)
    return None


def p2(d):
    steps = parse_steps(d)
    nodes = build_nodes(steps)
    workers = [Worker() for i in range(NUM_WORKERS)]
    time = 0
    ns = find_next_p2(nodes, workers)

    while not (all([w.node is None for w in workers]) and len(ns) == 0):
        # assign everything to workers
        for i in range(len(workers)):
            if len(ns) == 0:
                break
            if workers[i].node is None:
                workers[i].assign(ns[0])
                del ns[0]

        # tick
        for worker in workers:
            if worker.node is not None:
                worker.work()
                if worker.time_worked == worker.node.time:
                    worker.node.done = True
                    worker.done()

        time += 1
        ns = find_next_p2(nodes, workers)

    return time


def find_next_p2(nodes, workers):
    ready = []
    for node in nodes:
        if any([None != w.node and w.node == node for w in workers]):
            continue
        if node.done:
            continue
        elif len(node.prev) == 0:
            ready.append(node)
        else:
            if all(n.done for n in node.prev):
                ready.append(node)
    ready.sort()
    return ready


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
