import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    lst = list(map(int, input().split()))
    print(sum(lst))