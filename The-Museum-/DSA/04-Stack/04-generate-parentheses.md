# Generate Parentheses

**Difficulty:** Medium  
**Pattern:** Stack  
**LeetCode:** #22

## Problem Statement

Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

## Examples

### Example 1:
```
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

### Example 2:
```
Input: n = 1
Output: ["()"]
```

## Constraints

- `1 <= n <= 8`

## Solution Approaches

### Approach 1: Backtracking
**Time Complexity:** O(4^n / sqrt(n)) - Catalan number  
**Space Complexity:** O(n)

```python
def generateParenthesis(n):
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result
```

### Approach 2: Dynamic Programming
**Time Complexity:** O(4^n / sqrt(n))  
**Space Complexity:** O(4^n / sqrt(n))

```python
def generateParenthesis(n):
    dp = [[] for _ in range(n + 1)]
    dp[0] = ['']
    
    for i in range(1, n + 1):
        for j in range(i):
            for left in dp[j]:
                for right in dp[i - 1 - j]:
                    dp[i].append(f'({left}){right}')
    
    return dp[n]
```

### Approach 3: Iterative with Stack
**Time Complexity:** O(4^n / sqrt(n))  
**Space Complexity:** O(n)

```python
def generateParenthesis(n):
    result = []
    stack = [('', 0, 0)]  # (current_string, open_count, close_count)
    
    while stack:
        current, open_count, close_count = stack.pop()
        
        if len(current) == 2 * n:
            result.append(current)
            continue
        
        if close_count < open_count:
            stack.append((current + ')', open_count, close_count + 1))
        
        if open_count < n:
            stack.append((current + '(', open_count + 1, close_count))
    
    return result
```

## Key Insights

1. **Add opening** parenthesis if count < n
2. **Add closing** parenthesis if count < opening count
3. **Valid string** when length = 2n

## Related Problems

- Valid Parentheses (LeetCode #20)
- Letter Combinations of a Phone Number (LeetCode #17)
- Check if a Parentheses String Can Be Valid (LeetCode #2116)