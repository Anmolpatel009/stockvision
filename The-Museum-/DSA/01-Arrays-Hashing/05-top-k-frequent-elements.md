# Top K Frequent Elements

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #347

## Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

## Examples

### Example 1:
```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

### Example 2:
```
Input: nums = [1], k = 1
Output: [1]
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `k` is in the range `[1, the number of unique elements in the array]`.
- It is guaranteed that the answer is unique.

## Solution Approaches

### Approach 1: Hash Map + Heap
**Time Complexity:** O(n log k)  
**Space Complexity:** O(n)

```python
import heapq
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### Approach 2: Bucket Sort
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    freq = [[] for _ in range(len(nums) + 1)]
    
    for num, cnt in count.items():
        freq[cnt].append(num)
    
    result = []
    for i in range(len(freq) - 1, 0, -1):
        for num in freq[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

### Approach 3: Quick Select
**Time Complexity:** O(n) average, O(n²) worst case  
**Space Complexity:** O(n)

```python
from collections import Counter
import random

def topKFrequent(nums, k):
    count = Counter(nums)
    unique = list(count.keys())
    
    def partition(left, right, pivot_index):
        pivot_freq = count[unique[pivot_index]]
        unique[pivot_index], unique[right] = unique[right], unique[pivot_index]
        store_index = left
        
        for i in range(left, right):
            if count[unique[i]] < pivot_freq:
                unique[store_index], unique[i] = unique[i], unique[store_index]
                store_index += 1
        
        unique[right], unique[store_index] = unique[store_index], unique[right]
        return store_index
    
    def quickselect(left, right, k_smallest):
        if left == right:
            return
        
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)
        
        if k_smallest == pivot_index:
            return
        elif k_smallest < pivot_index:
            quickselect(left, pivot_index - 1, k_smallest)
        else:
            quickselect(pivot_index + 1, right, k_smallest)
    
    n = len(unique)
    quickselect(0, n - 1, n - k)
    return unique[n - k:]
```

## Key Insights

1. **Bucket sort** is optimal for this problem - O(n) time
2. **Heap** is simpler and works well when k is small
3. **Quick select** provides average O(n) but has worst case O(n²)

## Related Problems

- Kth Largest Element in an Array (LeetCode #215)
- Sort Characters By Frequency (LeetCode #451)
