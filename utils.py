def file_to_1d_array(path):
    arr = []
    with open(path) as f:
        for line in f:
            arr.append(line.strip())
    f.close()
    return arr


def file_to_2d_array(path):
    arr = []
    with open(path) as f:
        for line in f:
            arr.append(line.split())
    f.close()
    return arr


def flat_list(lists):
    return [item for sublist in lists for item in sublist]
