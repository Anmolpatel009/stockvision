# Find Minimum in Rotated Sorted Array

**Difficulty:** Medium  
**Pattern:** Binary Search  
**LeetCode:** #153

## Problem Statement

Suppose an array of length `n` sorted in ascending order is rotated between 1 and `n` times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

You must write an algorithm that runs in O(log n) time.

## Examples

### Example 1:
```
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.
```

### Example 2:
```
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.
```

### Example 3:
```
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.
```

## Constraints

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All the integers of `nums` are unique.
- `nums` is sorted and rotated between 1 and `n` times.

## Solution Approaches

### Approach 1: Binary Search
**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    
    return nums[left]
```

### Approach 2: Binary Search with Left Comparison
**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

```python
def findMin(nums):
    left, right = 0, len(nums) - 1
    
    # If not rotated
    if nums[left] < nums[right]:
        return nums[left]
    
    while left < right:
        mid = (left + right) // 2
        
        if nums[mid] >= nums[0]:
            left = mid + 1
        else:
            right = mid
    
    return nums[left]
```

### Approach 3: Linear Search (Not Optimal)
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def findMin(nums):
    return min(nums)
```

## Key Insights

1. **Compare mid with right** - if mid > right, minimum is in right half
2. **When mid <= right**, minimum is in left half (including mid)
3. **Loop ends** when left == right, pointing to minimum

## Related Problems

- Search in Rotated Sorted Array (LeetCode #33)
- Find Minimum in Rotated Sorted Array II (LeetCode #154)