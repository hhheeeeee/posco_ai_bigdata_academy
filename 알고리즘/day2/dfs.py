import sys
from collections import deque
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def dfs(graph, start, visited):
    visited[start] = True
    print(start, end = " ")
    for i in graph[start]:
        if not visited[i]:
            dfs(graph, i, visited)

t = int(input())
for _ in range(t):
    v, e = map(int, input().split())
    graph = [ [] for _ in range(v)]
    for _ in range(e):
        start, end = list(map(int, input().split()))
        graph[start].append(end)
        graph[end].append(start)
    for i in range(v):
        graph[i] = sorted(graph[i])
    visited = [False] * v
    dfs(graph, 0, visited)
    print()