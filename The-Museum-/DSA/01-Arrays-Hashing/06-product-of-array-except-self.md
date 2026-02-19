# Product of Array Except Self

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #238

## Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

You must write an algorithm that runs in O(n) time and without using the division operation.

## Examples

### Example 1:
```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

### Example 2:
```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

## Solution Approaches

### Approach 1: Left and Right Product Arrays
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def productExceptSelf(nums):
    n = len(nums)
    left = [1] * n
    right = [1] * n
    
    # Build left products
    for i in range(1, n):
        left[i] = left[i-1] * nums[i-1]
    
    # Build right products
    for i in range(n-2, -1, -1):
        right[i] = right[i+1] * nums[i+1]
    
    # Calculate result
    return [left[i] * right[i] for i in range(n)]
```

### Approach 2: O(1) Space (excluding output)
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
    
    # Calculate left products in result
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Calculate right products and multiply
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result
```

### Approach 3: Using Division (not allowed but shown for reference)
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def productExceptSelf(nums):
    total_product = 1
    zero_count = 0
    
    for num in nums:
        if num == 0:
            zero_count += 1
        else:
            total_product *= num
    
    result = []
    for num in nums:
        if zero_count > 1:
            result.append(0)
        elif zero_count == 1:
            result.append(0 if num != 0 else total_product)
        else:
            result.append(total_product // num)
    
    return result
```

## Key Insights

1. **Two-pass approach** - left products then right products
2. **O(1) space** by using result array for left products
3. **Division approach** handles zeros but violates problem constraints

## Related Problems

- Trapping Rain Water (LeetCode #42)
- Maximum Subarray (LeetCode #53)
