# House Robber

**Difficulty:** Medium  
**Pattern:** 1D Dynamic Programming  
**LeetCode:** #198

## Problem Statement
You are a robber planning to rob houses. Each house has money. You cannot rob adjacent houses. Return the maximum amount.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def rob(nums):
    if not nums:
        return 0
    if len(nums) <= 2:
        return max(nums)
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    return dp[-1]
```

### Approach 2: Space Optimized
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def rob(nums):
    prev, curr = 0, 0
    for num in nums:
        prev, curr = curr, max(curr, prev + num)
    return curr
```
