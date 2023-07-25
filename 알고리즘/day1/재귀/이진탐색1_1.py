import sys
#sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def binary_search(lst, search):
    low = 0
    high = len(lst) - 1

    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == search:
            return mid
        elif lst[mid] < search:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1

t = int(input())
for _ in range(t):
    lst = list(map(int, input().split()))
    search = list(map(int, input().split()))
    result = []
    for num in search:
        result.append(binary_search(lst, num))
    print(*result)