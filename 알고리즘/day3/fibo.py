import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def fibo(n, memo):
    for i in range(n+1):
        if i < 2:
            memo[i] = i
        else:
            memo[i] = memo[i-2] + memo[i-1]
    return memo[n]


t = int(input())
for _ in range(t):
    n = int(input())
    memo = [0] * (n+1)
    print(fibo(n, memo))
