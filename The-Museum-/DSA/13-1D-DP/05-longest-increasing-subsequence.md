# Longest Increasing Subsequence

**Difficulty:** Medium  
**Pattern:** 1D Dynamic Programming  
**LeetCode:** #300

## Problem Statement
Given an integer array nums, return the length of the longest strictly increasing subsequence.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(n²)  
**Space Complexity:** O(n)

```python
def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

### Approach 2: Binary Search
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
import bisect

def lengthOfLIS(nums):
    tails = []
    
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    
    return len(tails)
```
