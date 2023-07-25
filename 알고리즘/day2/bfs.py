import sys
from collections import deque
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True
    while queue:
        v = queue.popleft()
        print(v, end = " ")
        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

t = int(input())
for _ in range(t):
    v, e = map(int, input().split())
    graph = [ [] for _ in range(v)]
    for _ in range(e):
        start, end = list(map(int, input().split()))
        graph[start].append(end)
        #graph[end].append(start)
    for i in range(v):
        graph[i] = sorted(graph[i])
    visited = [False] * v
    bfs(graph, 0, visited)
    print()