import sys
#sys.stdin = open("prob1.txt", "r")
input = sys.stdin.readline

def make_road(cities):
    cost = 0
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            x = abs(cities[i][0] - cities[j][0])
            y = abs(cities[i][1] - cities[j][1])
            cost += (x + y)
    return cost

t = int(input())
for _ in range(t):
    n = int(input())
    cities = []
    for _ in range(n):
        x, y = map(int, input().split())
        cities.append((x,y))
        result = make_road(cities)
    print(result)