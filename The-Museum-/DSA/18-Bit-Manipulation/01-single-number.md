# Single Number

**Difficulty:** Easy  
**Pattern:** Bit Manipulation  
**LeetCode:** #136

## Problem Statement
Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

## Solution Approaches

### Approach 1: XOR
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

## Key Insights
1. XOR of a number with itself is 0
2. XOR of a number with 0 is the number itself
3. XOR is commutative and associative
