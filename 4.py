import re

BEGINS = 0
ASLEEP = 1
WAKE = 2


def parse_instruction(i):
    if 'begins' in i:
        return BEGINS
    elif 'asleep' in i:
        return ASLEEP
    else:
        return WAKE


def parse_record(record):
    match = re.match(r'\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] (.*)', record)
    guard = re.search(r'#(\d+)', record)
    return {
        "time": int(match.group(1)),
        "i": parse_instruction(match.group(2)),
        "g": int(guard.group(1)) if guard != None else None
    }


def p1(records):
    records.sort()
    guard_mins_asleep = {}
    guard_total_mins_asleep = {}
    curr_guard = None
    minute = 0

    for record in records:
        r = parse_record(record)
        if r["i"] == BEGINS:
            curr_guard = r["g"]
            if r["g"] not in guard_mins_asleep:
                guard_mins_asleep[curr_guard] = [0 for i in range(60)]
                guard_total_mins_asleep[curr_guard] = 0
            minute = 0
        elif r["i"] == ASLEEP:
            minute = r["time"]
        else:
            for i in range(minute, r["time"]):
                guard_mins_asleep[curr_guard][i] += 1
            guard_total_mins_asleep[curr_guard] += r["time"] - minute

    sleepiest_guard = max(guard_total_mins_asleep.items(),
                          key=lambda x: x[1])[0]

    sleepiest_minute = guard_mins_asleep[sleepiest_guard].index(
        max(guard_mins_asleep[sleepiest_guard]))

    return sleepiest_guard * sleepiest_minute


if __name__ == "__main__":
    import sys
    import utils
    part = sys.argv[1]
    records = utils.file_to_1d_array('inputs/4.txt')
    answer = p1(records) if part == '1' else 0
    print(answer)
