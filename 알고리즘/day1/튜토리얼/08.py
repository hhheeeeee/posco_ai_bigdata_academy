import sys
from collections import deque
#sys.stdin = open("01.txt", "r")
input = sys.stdin.readline

def two_race(race):
    q = deque()
    for i in race:
        if q and i == q[0]:
            q.popleft()
        else:
            q.append(i)                   
    return q

t = int(input())  
for _ in range(t):
    race = list(map(int, input().split())) 
    if two_race(race):
        print('YES')
    else:
        print('NO')