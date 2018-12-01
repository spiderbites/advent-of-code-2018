import utils

nums = utils.file_to_1d_array('inputs/1.txt')


def p1():
    return sum([int(num) for num in nums])


def p2():
    val = 0
    seen = set()
    seen.add(0)
    while True:
        for num in nums:
            val += int(num)
            if val in seen:
                return val
            seen.add(val)


print(p1())
print(p2())
