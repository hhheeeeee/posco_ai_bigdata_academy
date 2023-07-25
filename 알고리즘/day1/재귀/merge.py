import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def merge(fst, snd):
    result = []
    i, j = 0, 0

    while i < len(fst) and j < len(snd):
        if fst[i] < snd[j]:
            result.append(1)
            i += 1
        else:
            result.append(2)
            j += 1

    # 남은 원소들을 추가합니다.
    while i < len(fst):
        result.append(1)
        i += 1
    while j < len(snd):
        result.append(2)
        j += 1

    return result


input = sys.stdin.readline
t = int(input())

for _ in range(t):
    fst = list(map(int, input().split()))
    snd = list(map(int, input().split()))
    result = merge(fst, snd)
    print(*result)