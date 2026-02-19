# Unique Paths

**Difficulty:** Medium  
**Pattern:** 2D Dynamic Programming  
**LeetCode:** #62

## Problem Statement
A robot is located at the top-left corner of a m x n grid. Find the number of possible unique paths to reach the bottom-right corner.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(m * n)  
**Space Complexity:** O(m * n)

```python
def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]
```

### Approach 2: Space Optimized
**Time Complexity:** O(m * n)  
**Space Complexity:** O(n)

```python
def uniquePaths(m, n):
    row = [1] * n
    
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j-1]
    
    return row[-1]
```

### Approach 3: Math
```python
import math

def uniquePaths(m, n):
    return math.comb(m + n - 2, m - 1)
```
