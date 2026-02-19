# Two Sum

**Difficulty:** Easy  
**Pattern:** Arrays & Hashing  
**LeetCode:** #1

## Problem Statement

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Examples

### Example 1:
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

### Example 2:
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

### Example 3:
```
Input: nums = [3,3], target = 6
Output: [0,1]
```

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

## Solution Approaches

### Approach 1: Hash Map (One Pass)
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### Approach 2: Brute Force
**Time Complexity:** O(n²)  
**Space Complexity:** O(1)

```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

### Approach 3: Two Pointers (requires sorting, loses original indices)
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def twoSum(nums, target):
    indexed_nums = [(num, i) for i, num in enumerate(nums)]
    indexed_nums.sort(key=lambda x: x[0])
    
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        if current_sum == target:
            return [indexed_nums[left][1], indexed_nums[right][1]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

## Key Insights

1. **Hash Map** is optimal - single pass with O(n) time
2. Store each number's index as you iterate
3. Check if complement exists before adding current number to map

## Related Problems

- Two Sum II - Input Array Is Sorted (LeetCode #167)
- Two Sum III - Data structure design (LeetCode #170)
- Two Sum IV - Input is a BST (LeetCode #653)
