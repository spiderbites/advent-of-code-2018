def process_rules(rules):
    return [[list(l[0]), l[1]] for l in [line.strip().split(' => ') for line in rules]]


def p1(initial, rules):
    gens = 20
    rules = process_rules(rules)
    initial_length = len(initial)
    state = list('.' * gens + initial + '.' * gens)
    indices = range(-gens, initial_length + gens + 1)

    for _ in range(gens):
        changed = []
        newstate = state[:]
        for i in range(2, len(state)-1):
            for rule in rules:
                if state[(i-2):(i+3)] == rule[0]:
                    newstate[i] = rule[1]
                    changed.append(i)
                    break
        for i in range(len(state)):
            if i not in changed:
                newstate[i] = '.'
        state = newstate[:]

    return sum([index for (index, plant) in zip(indices, state) if plant == '#'])


def p2_generator(initial, rules):
    rules = process_rules(rules)
    initial_length = len(initial)
    gens = 250
    state = list('.' * gens + initial + '.' * gens)
    indices = range(-gens, initial_length + gens + 1)

    for g in range(1, gens):
        changed = []
        newstate = state[:]
        for i in range(2, len(state)-1):
            for rule in rules:
                if state[(i-2):(i+3)] == rule[0]:
                    newstate[i] = rule[1]
                    changed.append(i)
                    break
        for i in range(len(state)):
            if i not in changed:
                newstate[i] = '.'
        state = newstate[:]
        total = sum([index for (index, plant) in zip(
            indices, state) if plant == '#'])

        print("{0} : {1}".format(g, total))


def p2():
    return relation(50000000000)


def relation(generation):
    return (generation * 32) + (generation + 55)


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    initial = data[0].split('initial state: ')[1]
    rules = data[2:]
    answer = p1(initial, rules) if part == '1' else p2()

    # used the p2_generator to devise the relation
    # p2_generator(initial, rules)

    print(answer)
