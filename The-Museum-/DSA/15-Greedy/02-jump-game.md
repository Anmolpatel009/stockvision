# Jump Game

**Difficulty:** Medium  
**Pattern:** Greedy  
**LeetCode:** #55

## Problem Statement
You are given an integer array nums. Return true if you can reach the last index.

## Solution Approaches

### Approach 1: Greedy
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def canJump(nums):
    max_reach = 0
    
    for i, num in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + num)
        if max_reach >= len(nums) - 1:
            return True
    
    return True
```
