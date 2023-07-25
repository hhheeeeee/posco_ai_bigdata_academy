import sys
from collections import deque
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline
import heapq

def shortest_path(graph, start, end):
    INF = float('inf')
    n = len(graph)
    dist = [INF] * n  # 최단 거리를 저장하는 배열
    dist[start] = 0  # 시작 정점의 최단 거리는 0
    pq = [(0, start)]  # 우선순위 큐에 (거리, 정점)을 저장

    while pq:
        cost, node = heapq.heappop(pq)  # 가장 거리가 짧은 정점 선택
        if node == end:
            return dist[end]  # 도착 정점에 도달한 경우 최단 거리 반환

        # 현재 정점에서 인접한 정점들을 탐색
        for adjacent, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[adjacent]:
                dist[adjacent] = new_cost  # 최단 거리 갱신
                heapq.heappush(pq, (new_cost, adjacent))  # 우선순위 큐에 추가

    return -1  # 도착 정점에 도달할 수 없는 경우

# 입력 예시에 대한 테스트
t = int(input())  # 테스트 케이스 수

for _ in range(t):
    n, m = map(int, input().split())  # 정점의 개수, 간선의 개수
    graph = [[] for _ in range(n)]  # 그래프 초기화

    # 간선 정보 입력
    for _ in range(m):
        u, v, c = map(int, input().split())  # 출발 정점, 도착 정점, 가중치
        graph[u].append((v, c))  # 방향성 그래프이므로 한 방향으로만 추가

    result = shortest_path(graph, 0, n-1)  # 0번 정점에서 N-1번 정점까지의 최단 경로 탐색
    print(result)

