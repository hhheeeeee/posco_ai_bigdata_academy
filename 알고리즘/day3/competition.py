import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

# t = int(input())
# for _ in range(t):
#     n, m = map(int, input().split())
#     board = [list(map(int, input().split())) for _ in range(n)]
#     print(board)


for _ in range(int(input())):
    n, m = map(int, input().split())
    data = [list(map(int, input().split())) for _ in range(n)]
    # T[i][j] = 거기에 도달했을 때 잃을 수 있는 최소 점수
    T = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            #시작 칸 인 경우
            #제일 위쪽 또는 왼쪽 줄인 경우
            #그 외의경우
            if i == 0 and j == 0:
                T[i][j] = data[i][j]
            elif i == 0 and j > 0:
                T[i][j] = T[i][j-1] + data[i][j]
            elif i > 0  and j == 0:
                T[i][j] = T[i-1][j] + data[i][j]
            elif i > 0 and j > 0:
                T[i][j] = min(T[i][j-1],T[i-1][j],T[i-1][j-1]) + data[i][j]
    print(T[n-1][m-1])
    