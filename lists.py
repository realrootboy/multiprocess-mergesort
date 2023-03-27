def split_list(list, x):
    return [list[i::x] for i in range(x)]

def group_by_two(list):
    return zip(*[iter(list)]*2)