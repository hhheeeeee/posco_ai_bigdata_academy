import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def stack_operations(queries):
    stack = []
    result = []
    for query in queries:
        if query == -1:
            if stack:
                result.append(stack.pop())
        else:
            stack.append(query)
    print(*result)

t = int(input())  
for _ in range(t):
    n = int(input()) 
    queries = list(map(int, input().split())) 
    result = stack_operations(queries)
