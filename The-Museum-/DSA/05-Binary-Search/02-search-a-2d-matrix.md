# Search a 2D Matrix

**Difficulty:** Medium  
**Pattern:** Binary Search  
**LeetCode:** #74

## Problem Statement

You are given an `m x n` integer matrix `matrix` with the following two properties:

1. Each row is sorted in non-decreasing order.
2. The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` if `target` is in `matrix` or `false` otherwise.

You must write a solution in O(log(m * n)) time complexity.

## Examples

### Example 1:
```
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

### Example 2:
```
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

## Solution Approaches

### Approach 1: Single Binary Search
**Time Complexity:** O(log(m * n))  
**Space Complexity:** O(1)

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = (left + right) // 2
        row, col = mid // n, mid % n
        
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False
```

### Approach 2: Two Binary Searches
**Time Complexity:** O(log m + log n)  
**Space Complexity:** O(1)

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    
    # Binary search for the correct row
    top, bottom = 0, m - 1
    while top <= bottom:
        mid = (top + bottom) // 2
        if matrix[mid][0] > target:
            bottom = mid - 1
        elif matrix[mid][-1] < target:
            top = mid + 1
        else:
            break
    
    if top > bottom:
        return False
    
    row = (top + bottom) // 2
    
    # Binary search within the row
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        if matrix[row][mid] == target:
            return True
        elif matrix[row][mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False
```

### Approach 3: Search from Top-Right
**Time Complexity:** O(m + n)  
**Space Complexity:** O(1)

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1
    
    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            row += 1
        else:
            col -= 1
    
    return False
```

## Key Insights

1. **Flatten the matrix** conceptually for single binary search
2. **Row = mid // n, Col = mid % n** for index conversion
3. **Two-phase search** can be more intuitive

## Related Problems

- Search a 2D Matrix II (LeetCode #240)
- Find Peak Element (LeetCode #162)