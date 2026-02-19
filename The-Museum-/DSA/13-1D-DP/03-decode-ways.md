# Decode Ways

**Difficulty:** Medium  
**Pattern:** 1D Dynamic Programming  
**LeetCode:** #91

## Problem Statement
A message containing letters from A-Z can be encoded into numbers. Given a string s containing only digits, return the number of ways to decode it.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def numDecodings(s):
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]
    
    return dp[n]
```

### Approach 2: Space Optimized
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def numDecodings(s):
    if not s or s[0] == '0':
        return 0
    
    prev2, prev1 = 1, 1
    
    for i in range(1, len(s)):
        curr = 0
        if s[i] != '0':
            curr += prev1
        if 10 <= int(s[i-1:i+1]) <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr
    
    return prev1
```
