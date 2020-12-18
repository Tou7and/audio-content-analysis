

def sort_timestamps(time_stamps, head_index, tail_index, terminate=False):
    """ Sort time-stamps based on start time. 
    
    Use quick-sort and pivot is always the last.
    """
    if tail_index >= len(time_stamps):
        raise ValueError("tail_index must less or equal to length of timestamps.")

    print("Pivot val: {}".format(time_stamps[tail_index]))
    if tail_index > head_index:
        print(head_index, tail_index)
        pivot_index = tail_index
        counter = 0
        for index in range(head_index, tail_index):
            if time_stamps[index-counter]["start"] > time_stamps[pivot_index]["start"]:
                # time_stamps.append(time_stamps.pop(index-counter))
                bigger = time_stamps.pop(index-counter)
                time_stamps.insert(tail_index, bigger)
                pivot_index -= 1
                counter += 1
                print(time_stamps)
        print("Pivot: {}".format(pivot_index))
        sort_timestamps(time_stamps, head_index, pivot_index-1)
        sort_timestamps(time_stamps, pivot_index+1, tail_index)
    return time_stamps

ts1 = [
    {"start": 0.0},
    {"start": 9.0},
    {"start": 7.0},
    {"start": 5.0},
    {"start": 5.0},
    {"start": 6.0},
    {"start": 11.0},
    {"start": 19.0},
    {"start": 16.0}
]

ts1_sorted = [
    {"start": 0.0},
    {"start": 5.0},
    {"start": 5.0},
    {"start": 6.0},
    {"start": 7.0},
    {"start": 9.0},
    {"start": 11.0},
    {"start": 16.0},
    {"start": 19.0}
]

sort_timestamps(x, 0, len(x)-1)

