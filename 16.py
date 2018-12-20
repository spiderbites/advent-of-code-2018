import pdb


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


functions = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr
]

opcodes = []


def p1(data):
    i = 0
    total_matching_three = 0
    while i < len(data):
        equal = 0
        if data[i].startswith('Before'):
            before = eval(data[i].split('Before: ')[1])
            [_, *input] = [int(num) for num in data[i+1].split()]
            after = eval(data[i+2].split('After: ')[1])
            for f in functions:
                registers = before[:]
                f(registers, *input)
                if registers == after:
                    equal += 1
            if equal >= 3:
                total_matching_three += 1
            i += 3
        else:
            i += 1
    return total_matching_three


def p2(data):
    opcodes = [set(functions) for i in range(16)]
    i = 0
    while i < len(data):
        matching = set()
        if data[i].startswith('Before'):
            before = eval(data[i].split('Before: ')[1])
            [opcode, *input] = [int(num) for num in data[i+1].split()]
            after = eval(data[i+2].split('After: ')[1])
            for f in functions:
                registers = before[:]
                f(registers, *input)
                if registers == after:
                    matching.add(f)
            # the possible opcodes are the previously possible opcodes intersection the matching opcodes
            opcodes[opcode] = opcodes[opcode].intersection(matching)
            i += 3
        else:
            i += 1

    # determine which opcode is which
    opcodes = satisfy(opcodes)

    # skip ahead to the second section
    i = 0
    while data[i].startswith('Before'):
        i += 4
    i += 2

    # run the input against the resolved functions
    registers = [0, 0, 0, 0]
    while i < len(data):
        [opcode, *input] = [int(num) for num in data[i].split()]
        opcodes[opcode](registers, *input)
        i += 1

    return registers[0]


def satisfy(opcodes):
    # loop through the sets. if a set only contains one opcode, remove it from all other sets until each has just one
    while any(len(s) > 1 for s in opcodes):
        for (i, s) in enumerate(opcodes):
            if len(s) == 1:
                for j in range(len(opcodes)):
                    if i == j:
                        continue
                    opcodes[j] = opcodes[j] - opcodes[i]

    # return a list of functions, rather than a list of sets, each with one function
    return [list(o)[0] for o in opcodes]


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)

    print(answer)
