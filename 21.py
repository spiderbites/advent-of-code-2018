from functools import reduce
import pdb
from collections import Counter


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
    bound = int(data[0].split(' ')[1])
    ip = 0
    instructions = [instruction for instruction in data[1:]]
    instructions = [i.split(' ') for i in instructions]
    instructions = [[globals()[i[0]], int(i[1]), int(i[2]), int(i[3])]
                    for i in instructions]

    # by examination, the only instruction that involves register 0 is instruction 28:
    #   eqrr 4 0 2
    # By running the program with anything in register 0 until that instruction is hit
    # we see see something *different* happens if register 0 == register[4] (which is 12420065)
    # ergo...
    registers = [12420065, 0, 0, 0, 0, 0]
    i = 0
    while True:  # 1000000 * 100:
        print(registers[2])
        if ip >= len(instructions):
            break
        instruction = instructions[ip]
        registers[bound] = ip
        (op, *args) = instruction
        op(registers, *args)
        ip = registers[bound]
        ip += 1
        i += 1
    return registers, i, ip


def p2(data):
    bound = int(data[0].split(' ')[1])
    ip = 0
    instructions = [instruction for instruction in data[1:]]
    instructions = [i.split(' ') for i in instructions]
    instructions = [[globals()[i[0]], int(i[1]), int(i[2]), int(i[3])]
                    for i in instructions]

    registers = [0, 0, 0, 0, 0, 0]
    i = 0

    # Same observation as above...
    # Now we must find when the sequence of numbers that causes the
    # program to halt begins to repeat, and return the last non-repeating
    # number
    seen_values = {}
    last_non_repeating = None
    while True:
        if ip >= len(instructions):
            break
        instruction = instructions[ip]
        registers[bound] = ip
        if ip == 28:
            if registers[4] in seen_values:
                return last_non_repeating
            else:
                seen_values[registers[4]] = 0
                last_non_repeating = registers[4]
        (op, *args) = instruction
        op(registers, *args)
        ip = registers[bound]
        ip += 1

    return registers, i, ip


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    # note pt 2 takes a very long time...
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
