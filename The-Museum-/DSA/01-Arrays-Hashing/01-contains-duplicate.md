# Contains Duplicate

**Difficulty:** Easy  
**Pattern:** Arrays & Hashing  
**LeetCode:** #217

## Problem Statement

Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

## Examples

### Example 1:
```
Input: nums = [1,2,3,1]
Output: true
```

### Example 2:
```
Input: nums = [1,2,3,4]
Output: false
```

### Example 3:
```
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Solution Approaches

### Approach 1: Hash Set
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

### Approach 2: Sorting
**Time Complexity:** O(n log n)  
**Space Complexity:** O(1) or O(n) depending on sorting algorithm

```python
def containsDuplicate(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False
```

### Approach 3: Set Length Comparison
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def containsDuplicate(nums):
    return len(nums) != len(set(nums))
```

## Key Insights

1. **Hash Set** is the most efficient for this problem
2. **Sorting** approach uses less space but is slower
3. The set length comparison is the most concise Python solution

## Related Problems

- Contains Duplicate II (LeetCode #219)
- Contains Duplicate III (LeetCode #220)
