# import sys
# sys.stdin = open("prob3.txt", "r")
# input = sys.stdin.readline

def potential(nums, result):
    for i in range(len(nums)):
        if nums[i] == 1:
            result += 1
        if nums[i] == 2:
            if (nums[0] == 1 and i == 1) or (i == 0):
                result += 2
            else:
                result *= 2
        result %= 120509130217
    return result

t = int(input())
for _ in range(t):
    nums = list(map(int, input().split()))
    print(potential(nums , 0))