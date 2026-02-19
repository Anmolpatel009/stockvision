# Subsets II

**Difficulty:** Medium  
**Pattern:** Backtracking  
**LeetCode:** #90

## Problem Statement

Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

## Examples

### Example 1:
```
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
```

### Example 2:
```
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

## Solution Approaches

### Approach 1: Backtracking with Sorting
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n)

```python
def subsetsWithDup(nums):
    result = []
    nums.sort()
    
    def backtrack(start, current):
        result.append(current[:])
        
        for i in range(start, len(nums)):
            # Skip duplicates
            if i > start and nums[i] == nums[i-1]:
                continue
            
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result
```

### Approach 2: Iterative with Set
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n * 2^n)

```python
def subsetsWithDup(nums):
    result = [[]]
    nums.sort()
    
    for num in nums:
        new_subsets = []
        for subset in result:
            new_subset = subset + [num]
            if new_subset not in result:
                new_subsets.append(new_subset)
        result.extend(new_subsets)
    
    return result
```

### Approach 3: Counter-based
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n)

```python
from collections import Counter

def subsetsWithDup(nums):
    result = []
    count = Counter(nums)
    unique_nums = sorted(count.keys())
    
    def backtrack(index, current):
        if index == len(unique_nums):
            result.append(current[:])
            return
        
        num = unique_nums[index]
        # Don't include this number
        backtrack(index + 1, current)
        
        # Include this number 1 to count times
        for _ in range(count[num]):
            current.append(num)
            backtrack(index + 1, current)
        
        # Backtrack
        for _ in range(count[num]):
            current.pop()
    
    backtrack(0, [])
    return result
```

## Key Insights

1. **Sort first** to group duplicates together
2. **Skip duplicates** at same level: `i > start and nums[i] == nums[i-1]`
3. **Counter approach** handles duplicates naturally

## Related Problems

- Subsets (LeetCode #78)
- Combination Sum II (LeetCode #40)
- Permutations II (LeetCode #47)