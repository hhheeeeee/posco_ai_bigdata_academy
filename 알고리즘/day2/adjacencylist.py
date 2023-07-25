import sys
from collections import deque
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    v, e = map(int, input().split())
    result = [ [] for _ in range(v)]
    for _ in range(e):
        start, end = list(map(int, input().split()))
        result[start].append(end)
        result[end].append(start)
    for i in range(v):
        print(*sorted(result[i]))   

