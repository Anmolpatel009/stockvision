# Combination Sum

**Difficulty:** Medium  
**Pattern:** Backtracking  
**LeetCode:** #39

## Problem Statement

Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.

The same number may be chosen from `candidates` an unlimited number of times.

## Examples

### Example 1:
```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
```

### Example 2:
```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

## Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are distinct.
- `1 <= target <= 40`

## Solution Approaches

### Approach 1: Backtracking
**Time Complexity:** O(N^(T/M+1)) where N = len(candidates), T = target, M = min(candidates)  
**Space Complexity:** O(T/M)

```python
def combinationSum(candidates, target):
    result = []
    
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])  # i not i+1 because we can reuse
            current.pop()
    
    backtrack(0, [], target)
    return result
```

### Approach 2: Backtracking with Sorting
**Time Complexity:** O(N^(T/M+1))  
**Space Complexity:** O(T/M)

```python
def combinationSum(candidates, target):
    result = []
    candidates.sort()
    
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # Pruning since sorted
            
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()
    
    backtrack(0, [], target)
    return result
```

### Approach 3: Dynamic Programming
**Time Complexity:** O(N * T)  
**Space Complexity:** O(N * T)

```python
def combinationSum(candidates, target):
    dp = [[] for _ in range(target + 1)]
    dp[0] = [[]]
    
    for candidate in candidates:
        for i in range(candidate, target + 1):
            for combo in dp[i - candidate]:
                dp[i].append(combo + [candidate])
    
    return dp[target]
```

## Key Insights

1. **Can reuse same element** - pass same index in recursion
2. **Sort for pruning** - stop early if candidate > remaining
3. **Avoid duplicates** - only consider candidates from current index onwards

## Related Problems

- Combination Sum II (LeetCode #40)
- Combination Sum III (LeetCode #216)
- Combination Sum IV (LeetCode #377)