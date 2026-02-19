# Longest Common Subsequence

**Difficulty:** Medium  
**Pattern:** 2D Dynamic Programming  
**LeetCode:** #1143

## Problem Statement
Given two strings text1 and text2, return the length of their longest common subsequence.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(m * n)  
**Space Complexity:** O(m * n)

```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### Approach 2: Space Optimized
**Time Complexity:** O(m * n)  
**Space Complexity:** O(min(m, n))

```python
def longestCommonSubsequence(text1, text2):
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    
    prev = [0] * (len(text2) + 1)
    
    for c1 in text1:
        curr = [0] * (len(text2) + 1)
        for j, c2 in enumerate(text2):
            if c1 == c2:
                curr[j+1] = prev[j] + 1
            else:
                curr[j+1] = max(prev[j+1], curr[j])
        prev = curr
    
    return prev[-1]
```
