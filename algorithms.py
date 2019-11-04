def fcfs(arr):
    return arr


def look(arr):
    ret = []
    requests = arr[1:]
    end = max(requests)
    start = min(requests)
    for i in range(arr[0], end + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    for i in range(end, start - 1, -1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    ret.insert(0, arr[0])
    return ret


# SCAN
def scan(arr, end=40):
    requests = arr[1:]
    ret = []
    for i in range(arr[0], end + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    if end not in ret: ret.append(end)
    for i in range(end, 0, -1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    if 1 not in ret: ret.append(1)
    ret.insert(0, arr[0])
    return ret


# C-LOOK
def c_look(arr):
    ret = []
    requests = arr[1:]
    end = max(requests)
    start = min(requests)
    for i in range(arr[0], end + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    for i in range(start, arr[0] + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    ret.insert(0, arr[0])
    return ret


def c_scan(arr, end=40):
    ret = []
    requests = arr[1:]
    for i in range(arr[0], end + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    if end not in ret: ret.append(end)
    if 1 not in requests: ret.append(1)
    for i in range(1, arr[0] + 1):
        while i in requests:
            ret.append(i)
            requests.remove(i)
    ret.insert(0, arr[0])
    return ret


def sstf(arr):
    ret = []
    requests = arr[1:]
    ret.append(arr[0])
    while len(ret) != len(arr):
        head = ret[-1]
        next_head = min(requests, key=lambda x: abs(head - x))
        print(next_head)
        requests.remove(next_head)
        ret.append(next_head)
    return ret


def optimal(arr):
    head = arr[0]
    requests = sorted(arr[1:])
    if head - requests[0] < requests[-1] - head:
        return [arr[0]] + [i for i in requests if i < head][::-1] + [i for i in requests if i >= head]
    else:
        return [arr[0]] + [i for i in requests if i >= head] + [i for i in requests if i < head][::-1]

if __name__ == "__main__":
    seq = [25, 4, 30, 33, 5, 20, 7, 15, 31, 35, 28, 17]
    print(optimal(seq))
