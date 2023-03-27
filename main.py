from files import read_file
from lists import split_list
from multiprocess_sort import multiprocess_sort

def main():
    n_processes = 16
    n_values = 20
    lists = split_list(read_file('input.txt', n_values), n_processes)
    sorted_list = multiprocess_sort(lists)
    print(sorted_list)

if __name__ == '__main__':
    main()