# Maximum Subarray

**Difficulty:** Medium  
**Pattern:** Greedy  
**LeetCode:** #53

## Problem Statement
Given an integer array nums, find the subarray with the largest sum, and return its sum.

## Solution Approaches

### Approach 1: Kadane's Algorithm
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def maxSubArray(nums):
    max_sum = nums[0]
    curr_sum = nums[0]
    
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

### Approach 2: DP
```python
def maxSubArray(nums):
    dp = nums[:]
    for i in range(1, len(nums)):
        dp[i] = max(dp[i], dp[i-1] + nums[i])
    return max(dp)
```
