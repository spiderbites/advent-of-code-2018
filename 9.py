from collections import deque


def p1(total_players, last):
    marbles = deque([0])
    scores = {}
    curr_player = 1

    for i in range(1, total_players + 1):
        scores[i] = 0

    for turn in range(1, last + 1):
        if turn % 23 != 0:
            marbles.rotate(-1)
            marbles.append(turn)
        else:
            marbles.rotate(7)
            v = marbles.pop()
            marbles.rotate(-1)
            curr_player = (turn % total_players) + 1
            scores[curr_player] += turn + v

    return max(scores.values())


if __name__ == "__main__":
    import sys
    [part, f, ] = sys.argv[1:]
    f = open(f, 'r')

    if part == '1':
        players = 452
        last = 70784
        answer = p1(players, last)
    else:
        players = 452
        last = 70784 * 100
        answer = p1(players, last)

    print(answer)
