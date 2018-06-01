import sys
import re
import math
import heapq


def countOpens(f):
    n = 0
    for line in f:
        if line.startswith('open'):
            n += 1
    return n


def countDecil(n, file):
    listSize = math.ceil(0.1 * n)
    decil = []
    for line in file:
        if line.startswith('open'):
            time = float(re.search(r'\d+ usec', line).group(0).split(' ')[0])
            if len(decil) <= listSize:
                heapq.heappush(decil, time)
            else:
                min = decil[0]
                if time > min:
                    heapq.heappop(decil)
                    heapq.heappush(decil, time)
    return decil[-1]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Enter file path")
        filename = input()
    else:
        filename = sys.argv[1]
    with open(filename) as file:
        n = countOpens(file)
    with open(filename) as file:
        d = countDecil(n, file)
        print(d)
