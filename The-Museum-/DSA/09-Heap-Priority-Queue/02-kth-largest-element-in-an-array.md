# Kth Largest Element in an Array

**Difficulty:** Medium  
**Pattern:** Heap / Priority Queue  
**LeetCode:** #215

## Problem Statement

Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.

Note that it is the `k`th largest element in the sorted order, not the `k`th distinct element.

## Examples

### Example 1:
```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

### Example 2:
```
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

## Constraints

- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

## Solution Approaches

### Approach 1: Min Heap
**Time Complexity:** O(n log k)  
**Space Complexity:** O(k)

```python
import heapq

def findKthLargest(nums, k):
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]
```

### Approach 2: Max Heap
**Time Complexity:** O(n + k log n)  
**Space Complexity:** O(n)

```python
import heapq

def findKthLargest(nums, k):
    max_heap = [-num for num in nums]
    heapq.heapify(max_heap)
    
    for _ in range(k - 1):
        heapq.heappop(max_heap)
    
    return -max_heap[0]
```

### Approach 3: Quick Select
**Time Complexity:** O(n) average, O(n²) worst case  
**Space Complexity:** O(1)

```python
import random

def findKthLargest(nums, k):
    def partition(left, right, pivot_index):
        pivot = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        store_index = left
        
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index
    
    def select(left, right, k_smallest):
        if left == right:
            return nums[left]
        
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            return select(left, pivot_index - 1, k_smallest)
        else:
            return select(pivot_index + 1, right, k_smallest)
    
    return select(0, len(nums) - 1, len(nums) - k)
```

## Key Insights

1. **Min heap of size k** is most efficient for large n
2. **Quick select** provides average O(n) time
3. **Max heap** requires storing all elements

## Related Problems

- Kth Largest Element in a Stream (LeetCode #703)
- Top K Frequent Elements (LeetCode #347)
- K Closest Points to Origin (LeetCode #973)