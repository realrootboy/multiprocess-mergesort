def read_file(filename, n_values):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(int(line.strip()))
    return lines[:n_values]
