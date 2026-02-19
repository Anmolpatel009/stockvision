# Container With Most Water

**Difficulty:** Medium  
**Pattern:** Two Pointers  
**LeetCode:** #11

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

## Examples

### Example 1:
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The max area is formed by height[1] = 8 and height[8] = 7.
```

### Example 2:
```
Input: height = [1,1]
Output: 1
```

## Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Solution Approaches

### Approach 1: Two Pointers
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def maxArea(height):
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        min_height = min(height[left], height[right])
        max_area = max(max_area, width * min_height)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

### Approach 2: Brute Force
**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

```python
def maxArea(height):
    max_area = 0
    n = len(height)
    
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            min_height = min(height[i], height[j])
            max_area = max(max_area, width * min_height)
    
    return max_area
```

### Approach 3: Two Pointers with Early Termination
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def maxArea(height):
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        h = min(height[left], height[right])
        max_area = max(max_area, h * (right - left))
        
        # Skip lines that are shorter than current min
        while left < right and height[left] <= h:
            left += 1
        while left < right and height[right] <= h:
            right -= 1
    
    return max_area
```

## Key Insights

1. **Move the shorter line** - this is the key insight
2. **Area = min(height[left], height[right]) * (right - left)**
3. Moving the taller line can only decrease or maintain area

## Related Problems

- Trapping Rain Water (LeetCode #42)
- Trapping Rain Water II (LeetCode #407)