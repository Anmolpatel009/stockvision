# Search in Rotated Sorted Array

**Difficulty:** Medium  
**Pattern:** Binary Search  
**LeetCode:** #33

## Problem Statement

There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with O(log n) runtime complexity.

## Examples

### Example 1:
```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

### Example 2:
```
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

### Example 3:
```
Input: nums = [1], target = 0
Output: -1
```

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

## Solution Approaches

### Approach 1: Single Binary Search
**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```

### Approach 2: Find Pivot Then Binary Search
**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

```python
def search(nums, target):
    def find_pivot():
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return left
    
    def binary_search(left, right):
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    if not nums:
        return -1
    
    pivot = find_pivot()
    
    if nums[pivot] == target:
        return pivot
    
    if pivot == 0:
        return binary_search(0, len(nums) - 1)
    
    if target >= nums[0]:
        return binary_search(0, pivot - 1)
    else:
        return binary_search(pivot, len(nums) - 1)
```

### Approach 3: Recursive
**Time Complexity:** O(log n)  
**Space Complexity:** O(log n)

```python
def search(nums, target):
    def helper(left, right):
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                return helper(left, mid - 1)
            else:
                return helper(mid + 1, right)
        else:
            if nums[mid] < target <= nums[right]:
                return helper(mid + 1, right)
            else:
                return helper(left, mid - 1)
    
    return helper(0, len(nums) - 1)
```

## Key Insights

1. **One half is always sorted** in rotated array
2. **Check which half is sorted** then determine if target is in that half
3. **Pivot finding** can be done separately

## Related Problems

- Find Minimum in Rotated Sorted Array (LeetCode #153)
- Search in Rotated Sorted Array II (LeetCode #81)