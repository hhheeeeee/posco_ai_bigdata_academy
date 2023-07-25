# import sys
# sys.stdin = open("prob3.txt", "r")
# input = sys.stdin.readline

MOD = 120509130217

def calculate_potential(nums):
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]

    for i in range(1, n):
        dp[i] = max(dp[i-1] +nums[i], (dp[i-1] * nums[i])) % MOD

    return dp[-1]

t = int(input())
for _ in range(t):
    nums = list(map(int, input().split()))
    result = calculate_potential(nums)
    print(result)
