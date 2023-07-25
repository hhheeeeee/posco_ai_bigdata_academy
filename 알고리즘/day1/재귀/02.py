import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def hanoi(n, start, mid, end):
    if n == 1: #남은 하나를 start에서 end로 옮김
        print(start,'->',end)
    
    else:
        hanoi(n-1, start, end, mid) #n-1개의 고리를 start에서 mid로 옮김
        print(start,'->',mid)
        hanoi(n-1, end, mid ,start) #mid로 옮긴 n-1개 고리를 end로 옮김


t = int(input())
for _ in range(t):
    a = int(input())
    hanoi(a, 'A','B','C')