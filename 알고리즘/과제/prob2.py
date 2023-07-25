import sys
#sys.stdin = open("prob2.txt", "r")
input = sys.stdin.readline

def virus(graph,visited, k):
    visited[k] = True
    for i in graph[k]:
        if not visited[i]:
            virus(graph, visited, i)

T = int(input())
for _ in range(T):
    n, m, k = map(int, input().split())
    visited = [False] * (n)
    graph = [[] for _ in range(n)]
    for _ in range(m):
        start, end = map(int, input().split())
        graph[start].append(end)
        graph[end].append(start)
    virus(graph, visited, k)
    cnt = 0
    for v in visited:
        if not v:
            cnt += 1
    print(cnt)
