import sys
from collections import deque
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    v, e = map(int, input().split())
    result = [ [0] * v for _ in range(v)]
    for _ in range(e):
        line = list(map(int, input().split()))
        start, end = line[0], line[1]
        if len(line) == 2:
            cost = 0
        else:
            cost = line[2]
        result[start][end] = cost
    for i in range(v):
        print(*result[i])   

