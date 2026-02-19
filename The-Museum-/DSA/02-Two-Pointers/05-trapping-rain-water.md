# Trapping Rain Water

**Difficulty:** Hard  
**Pattern:** Two Pointers  
**LeetCode:** #42

## Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

## Examples

### Example 1:
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. 
In this case, 6 units of rain water are being trapped.
```

### Example 2:
```
Input: height = [4,2,0,3,2,5]
Output: 9
```

## Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

## Solution Approaches

### Approach 1: Two Pointers
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    
    return water
```

### Approach 2: Dynamic Programming
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def trap(height):
    if not height:
        return 0
    
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    
    return water
```

### Approach 3: Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def trap(height):
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            min_height = min(height[left], h) - height[bottom]
            water += width * min_height
        stack.append(i)
    
    return water
```

## Key Insights

1. **Water at each position** = min(max_left, max_right) - height[i]
2. **Two pointers** is most space-efficient
3. **Move pointer with smaller max** - guarantees correct calculation

## Related Problems

- Container With Most Water (LeetCode #11)
- Trapping Rain Water II (LeetCode #407)
- Pour Water (LeetCode #755)