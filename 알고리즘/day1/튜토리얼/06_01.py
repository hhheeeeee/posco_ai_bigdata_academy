import sys
import heapq
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def queue_operations(queries):
    hq = []
    result = []
    for query in queries:
        if query == -1:
            if hq:
                #hq.sort()
                result.append(heapq.heappop(hq))
        else:
            heapq.heappush(hq, query)
    print(*result)

t = int(input())  
for _ in range(t):
    n = int(input()) 
    queries = list(map(int, input().split())) 
    result = queue_operations(queries)
