def p1(recipes, after):
    e1 = 0
    e2 = 1
    while len(recipes) < after + 10:
        new_sum = recipes[e1] + recipes[e2]
        new_digits = str(new_sum)
        for char in new_digits:
            recipes.append(int(char))
        e1 = (e1 + recipes[e1] + 1) % len(recipes)
        e2 = (e2 + recipes[e2] + 1) % len(recipes)
    return ''.join([str(i) for i in recipes[-10:]])


def p2(recipes, after):
    e1 = 0
    e2 = 1
    after = [int(i) for i in list(str(after))]
    l = len(after)
    while True:
        new_sum = recipes[e1] + recipes[e2]
        new_digits = str(new_sum)
        for char in new_digits:
            recipes.append(int(char))
        e1 = (e1 + recipes[e1] + 1) % len(recipes)
        e2 = (e2 + recipes[e2] + 1) % len(recipes)
        if recipes[-l:] == after:
            return len(recipes) - l
        elif recipes[-l-1:-1] == after:
            return len(recipes) - l - 1


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    recipes = [3, 7]
    afterp1 = 165061
    afterp2 = '165061'
    answer = p1(recipes, afterp1) if part == '1' else p2(recipes, afterp2)
    print(answer)
