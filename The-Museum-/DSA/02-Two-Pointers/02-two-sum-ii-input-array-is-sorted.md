# Two Sum II - Input Array Is Sorted

**Difficulty:** Medium  
**Pattern:** Two Pointers  
**LeetCode:** #167

## Problem Statement

Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array `[index1, index2]` of length 2.

## Examples

### Example 1:
```
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
```

### Example 2:
```
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore, index1 = 1, index2 = 3. We return [1, 3].
```

### Example 3:
```
Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore, index1 = 1, index2 = 2. We return [1, 2].
```

## Constraints

- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`
- `numbers` is sorted in non-decreasing order.
- `-1000 <= target <= 1000`

## Solution Approaches

### Approach 1: Two Pointers
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def twoSum(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return [-1, -1]
```

### Approach 2: Binary Search
**Time Complexity:** O(n log n)  
**Space Complexity:** O(1)

```python
def twoSum(numbers, target):
    for i in range(len(numbers)):
        complement = target - numbers[i]
        left, right = i + 1, len(numbers) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if numbers[mid] == complement:
                return [i + 1, mid + 1]
            elif numbers[mid] < complement:
                left = mid + 1
            else:
                right = mid - 1
    
    return [-1, -1]
```

### Approach 3: Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def twoSum(numbers, target):
    seen = {}
    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return [seen[complement] + 1, i + 1]
        seen[num] = i
    return [-1, -1]
```

## Key Insights

1. **Two pointers** is optimal for sorted arrays - O(n) time, O(1) space
2. **Binary search** works but is slower
3. **Hash map** doesn't leverage sorted property

## Related Problems

- Two Sum (LeetCode #1)
- 3Sum (LeetCode #15)
- 4Sum (LeetCode #18)