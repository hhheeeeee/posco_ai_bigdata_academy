import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    coins = [50000, 10000, 5000, 1000, 500, 100]
    coinnum = 0
    for coin in coins:
        coinnum += n // coin
        n %= coin
    print(coinnum)
    