# Climbing Stairs

**Difficulty:** Easy  
**Pattern:** 1D Dynamic Programming  
**LeetCode:** #70

## Problem Statement
You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. In how many distinct ways can you climb to the top?

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def climbStairs(n):
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

### Approach 2: Space Optimized
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def climbStairs(n):
    if n <= 2:
        return n
    
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    
    return curr
```
