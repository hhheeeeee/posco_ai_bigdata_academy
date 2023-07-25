import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline
a, b = map(int, input().split())
print(a+b)