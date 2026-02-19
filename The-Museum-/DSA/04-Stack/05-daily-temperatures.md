# Daily Temperatures

**Difficulty:** Medium  
**Pattern:** Stack  
**LeetCode:** #739

## Problem Statement

Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature.

If there is no future day for which this is possible, keep `answer[i] == 0` instead.

## Examples

### Example 1:
```
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

### Example 2:
```
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
```

### Example 3:
```
Input: temperatures = [30,60,90]
Output: [1,1,0]
```

## Constraints

- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

## Solution Approaches

### Approach 1: Monotonic Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []  # Stack of indices
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_index = stack.pop()
            answer[prev_index] = i - prev_index
        stack.append(i)
    
    return answer
```

### Approach 2: Brute Force
**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    
    return answer
```

### Approach 3: Optimized with Array
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    hottest = 0
    
    for i in range(n - 1, -1, -1):
        if temperatures[i] >= hottest:
            hottest = temperatures[i]
            continue
        
        days = 1
        while temperatures[i + days] <= temperatures[i]:
            days += answer[i + days]
        answer[i] = days
    
    return answer
```

## Key Insights

1. **Monotonic decreasing stack** - stores indices of decreasing temperatures
2. **Pop when warmer** found - calculate days difference
3. **Process right to left** for alternative approach

## Related Problems

- Next Greater Element I (LeetCode #496)
- Next Greater Element II (LeetCode #503)
- Online Stock Span (LeetCode #901)