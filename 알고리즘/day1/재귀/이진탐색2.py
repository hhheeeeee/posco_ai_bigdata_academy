import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

INF = 10e9

def find_closest(lst, target):
    left = 0
    right = len(lst) - 1
    closest = INF

    while left <= right:
        mid = (left + right) // 2
        diff = abs(lst[mid] - target)

        if diff < closest:
            closest = diff
            result = lst[mid]
        elif diff == closest:
            result = min(result, lst[mid])

        if lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

t = int(input())
for _ in range(t):
    lst = list(map(int, input().split()))
    search = list(map(int, input().split()))
    result = []
    for num in search:
        closest = find_closest(lst, num)
        result.append(closest)
    print(*result)
