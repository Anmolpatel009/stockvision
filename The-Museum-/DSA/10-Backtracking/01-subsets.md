# Subsets

**Difficulty:** Medium  
**Pattern:** Backtracking  
**LeetCode:** #78

## Problem Statement

Given an integer array `nums` of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

## Examples

### Example 1:
```
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

### Example 2:
```
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

## Solution Approaches

### Approach 1: Backtracking
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n)

```python
def subsets(nums):
    result = []
    
    def backtrack(start, current):
        result.append(current[:])
        
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result
```

### Approach 2: Iterative
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n * 2^n)

```python
def subsets(nums):
    result = [[]]
    
    for num in nums:
        new_subsets = []
        for subset in result:
            new_subsets.append(subset + [num])
        result.extend(new_subsets)
    
    return result
```

### Approach 3: Bit Manipulation
**Time Complexity:** O(n * 2^n)  
**Space Complexity:** O(n * 2^n)

```python
def subsets(nums):
    n = len(nums)
    result = []
    
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result
```

## Key Insights

1. **Each element** can be either included or excluded
2. **2^n total subsets** for n elements
3. **Backtracking builds** subsets incrementally

## Related Problems

- Subsets II (LeetCode #90)
- Permutations (LeetCode #46)
- Combination Sum (LeetCode #39)