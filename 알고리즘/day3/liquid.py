import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    N, C = map(int, input().split())
    liquidlist = []
    for i in range(N):
        w, v = map(int, input().split())
        liquidlist.append((w/v, w, v))
    liquidlist.sort(reverse=True)
    maxg = 0
    for i in range(N): #현재 용액을 전부 넣을 수 있는 경우
        if  C >= liquidlist[i][2]:
            maxg += liquidlist[i][1]
            C -= liquidlist[i][2]
        else: #현재 용액을 일부만 넣을 수 있는 경우
            maxg += C*(liquidlist[i][0])
            break
    print(int(maxg))