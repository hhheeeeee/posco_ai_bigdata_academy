import sys
sys.stdin = open('01.txt','r')
input = sys.stdin.readline

def binary(data, left, right, q): #data의 left, right 범위 내에서 q의 위치를 반환
    if left > right:
        return -1
    mid = (left + right) // 2
    if data[mid] == q:
        return mid
    if data[mid] > q:
        subproblem = binary(data, left, mid-1, q)
    elif data[mid] < q:
        subproblem = binary(data, mid+1, right, q)
    return subproblem