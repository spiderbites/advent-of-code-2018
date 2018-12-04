import re


def p1(claims):
    mp = build_map(claims)
    return sum(len(v) > 1 for v in mp.values())


def build_map(claims):
    mp = {}
    for claim in claims:
        parsed = parse_claim(claim)
        squares = get_covered_squares(parsed)
        for square in squares:
            if square in mp:
                mp[square].append(parsed["id"])
            else:
                mp[square] = [parsed["id"]]
    return mp


def p2(claims):
    mp = build_map(claims)
    no_overlaps = set(
        flat_list(list(filter(lambda x: len(x) == 1, mp.values()))))
    overlaps = set(
        flat_list(list(filter(lambda x: len(x) > 1, mp.values()))))
    return no_overlaps - overlaps


def parse_claim(claim):
    match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim)
    return {
        "id": int(match.group(1)),
        "left": int(match.group(2)),
        "top": int(match.group(3)),
        "width": int(match.group(4)),
        "height": int(match.group(5)),
    }


def get_covered_squares(claim):
    return [serialize(x, y) for x in range(claim["left"], claim["left"] + claim["width"]) for y in range(claim["top"], claim["top"] + claim["height"])]


def serialize(x, y):
    return "{0}:{1}".format(x, y)


def flat_list(lists):
    return [item for sublist in lists for item in sublist]


if __name__ == "__main__":
    import sys
    [part, f] = sys.argv[1:]
    f = open(f, 'r')
    data = [line.strip() for line in f.readlines()]
    answer = p1(data) if part == '1' else p2(data)
    print(answer)
