from functools import reduce


def factors(n):
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    registers[c] = registers[a]


def seti(registers, a, b, c):
    registers[c] = a


def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0


def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0


def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0


def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0


def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0


def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0


def p1(data):
    registers = [0] * 6
    bound = int(data[0].split(' ')[1])
    ip = 0
    instructions = [instruction for instruction in data[1:]]
    instructions = [i.split(' ') for i in instructions]
    instructions = [[globals()[i[0]], int(i[1]), int(i[2]), int(i[3])]
                    for i in instructions]

    while True:
        if ip >= len(instructions):
            break
        instruction = instructions[ip]
        registers[bound] = ip
        (op, *args) = instruction
        op(registers, *args)
        ip = registers[bound]
        ip += 1

    return registers[0]


def p2(data):
    # initially this:
    registers = [1, 0, 0, 0, 0, 0]
    ip = 0

    # after running a while noticed it gets to this place:
    registers = [0, 0, 10551389, 2, 10551389, 1]
    ip = 3

    # shortly after that it flips to this, important b/c register 0 changes:
    registers = [1, 0, 12, 2, 10551389, 2]
    ip = 3

    # a while after that...
    registers = [1, 0, 698622, 7, 10551389, 3]
    ip = 8

    # so the last number is incrementing very slowly.
    # when it is greater than index 4, program will eventually
    # break. need to figure out what happens to register 0
    # throughout that time.

    # run that a while....
    # ([1, 0, 125012, 2, 10551389, 2], 3)

    # WHAT IS HAPPENING?
    # - index 2 "quickly" cycles up
    # - index 5 slowly cycles up.
    # - when index 5 is > index 4, the prgram breaks

    # IDEA
    # How many times does register 2 * 5 (-> 1) result in register 1 and 4 being equal?
    # that causes instruction 7 to happen, which adds the value of register 5 to
    # register 0

    # FACTORS OF 10551389: (1, 10551389), (363841, 29)

    # WHAT HAPPENS WHEN THIS LAST REGISTER IS 29?
    registers = [1, 0, 1, 2, 10551389, 29]
    ip = 3

    # IT CHANGES! 29 gets added to register 0:
    # WHAT HAPPENS WHEN THIS LAST REGISTER IS 363841?
    registers = [30, 0, 1, 2, 10551389, 363841]
    ip = 3

    # IT CHANGES: 363841 gets added, the next factor is 10551389 itself
    registers = [363871, 0, 1, 2, 10551389, 10551389]
    ip = 3

    # IT CHANGES AGAIN, now run it til it breaks
    registers = [10915260, 0, 1, 2, 10551389, 10551390]
    ip = 3

    bound = int(data[0].split(' ')[1])
    instructions = [instruction for instruction in data[1:]]
    instructions = [i.split(' ') for i in instructions]
    instructions = [[globals()[i[0]], int(i[1]), int(i[2]), int(i[3])]
                    for i in instructions]

    while True:
        if ip >= len(instructions):
            break
        instruction = instructions[ip]
        registers[bound] = ip
        (op, *args) = instruction
        op(registers, *args)
        ip = registers[bound]
        ip += 1
    return registers, ip


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
