# Permutations

**Difficulty:** Medium  
**Pattern:** Backtracking  
**LeetCode:** #46

## Problem Statement

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

## Examples

### Example 1:
```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Example 2:
```
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

## Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are unique.

## Solution Approaches

### Approach 1: Backtracking with Used Array
**Time Complexity:** O(n * n!)  
**Space Complexity:** O(n)

```python
def permute(nums):
    result = []
    used = [False] * len(nums)
    
    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack(current)
                current.pop()
                used[i] = False
    
    backtrack([])
    return result
```

### Approach 2: Swapping In-Place
**Time Complexity:** O(n * n!)  
**Space Complexity:** O(n!)

```python
def permute(nums):
    result = []
    
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result
```

### Approach 3: Python itertools
**Time Complexity:** O(n!)  
**Space Complexity:** O(n!)

```python
from itertools import permutations

def permute(nums):
    return [list(p) for p in permutations(nums)]
```

## Key Insights

1. **n! permutations** for n elements
2. **Track used elements** to avoid duplicates
3. **Swap approach** avoids extra space for tracking

## Related Problems

- Permutations II (LeetCode #47)
- Next Permutation (LeetCode #31)
- Permutation Sequence (LeetCode #60)