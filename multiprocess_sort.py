from multiprocessing import Process, Queue
import os

from lists import group_by_two

verbose = True
# f is a function that takes a list as an argument
# and sorts it
def f(list, queue):
    if verbose:
        print('child process', os.getpid())
        print('sorting list on child process pid', os.getpid())
    list.sort()
    queue.put(list)
    if verbose:
        print('sorted list on child process pid', os.getpid(), list)

# g is a function that takes two lists as arguments
# and merges them
def g(a, b, queue):
    if verbose:
        print('child process', os.getpid())
        print('merging lists on child process pid', os.getpid())
    c = []
    while len(a) > 0 and len(b) > 0:
        if a[0] < b[0]:
            c.append(a[0])
            a.pop(0)
        else:
            c.append(b[0])
            b.pop(0)
    if len(a) > 0:
        c.extend(a)
    else:
        c.extend(b)
    queue.put(c)
    if verbose:
        print('merged lists on child process pid', os.getpid(), c)
        print('\n')

def multiprocess_sort(lists):
    # for each list in lists, create a process to sort it
    # and add the process to the processes list
    processes = []
    queue = Queue()
    for list in lists:
        p = Process(target=f, args=(list, queue))
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()

    # get the sorted lists from the queue
    sorted_lists = []
    while not queue.empty():
        sorted_lists.append(queue.get())

    if verbose:
        print('parent process', os.getpid())
        print('all child processes finished')
        print('lists after sorting', sorted_lists)
        print('\n')

    round_number = 1

    # while there is more than one list in sorted_lists
    while len(sorted_lists) > 1:
        if verbose:
            print('now, we will launch a new process to merge lists two by two')
        zip_lists = group_by_two(sorted_lists)

        # for each pair of lists in zip_lists, create a process to merge them
        # and add the process to the processes list
        processes = []
        queue = Queue()

        for a, b in zip_lists:
            p = Process(target=g, args=(a, b, queue))
            processes.append(p)
            p.start()
    
        # wait for all processes to finish
        for p in processes:
            p.join()

        # get the merged lists from the queue
        merged_lists = []
        while not queue.empty():
            merged_lists.append(queue.get())

        # if there is an odd number of lists in sorted_lists,
        # add the last list to merged_lists
        if len(sorted_lists) % 2 == 1:
            merged_lists.append(sorted_lists[-1])

        if verbose:
            print('parent process', os.getpid())
            print('all child processes finished')
            print('lists after merging', merged_lists)
            print('\n')
    
        sorted_lists = merged_lists
        round_number += 1

    return sorted_lists[0]