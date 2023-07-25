import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def fibo(n):
    if n <= 1:
        return n
    return fibo(n-1)+fibo(n-2)


t = int(input())
for _ in range(t):
    print(fibo(int(input())))