import sys
sys.stdin = open("01.txt", "r")
input = sys.stdin.readline

def is_valid_parentheses(s):
    stack = []
    pairs = {'(': ')', '{': '}', '[': ']'}
    
    for char in s:
        if char in pairs:
            stack.append(char) 
        else:
            if not stack or pairs[stack.pop()] != char:  
                return "NO"  
    
    if stack:  
        return "NO"
    else:
        return "YES"

t = int(input())

for _ in range(t):
    parentheses = input().strip()  
    result = is_valid_parentheses(parentheses)  
    print(result)  
