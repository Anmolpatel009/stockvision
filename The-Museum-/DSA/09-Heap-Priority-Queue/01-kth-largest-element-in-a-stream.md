# Kth Largest Element in a Stream

**Difficulty:** Easy  
**Pattern:** Heap / Priority Queue  
**LeetCode:** #703

## Problem Statement

Design a class to find the `k`th largest element in a stream. Note that it is the `k`th largest element in the sorted order, not the `k`th distinct element.

Implement `KthLargest` class:
- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the `k`th largest element in the stream.

## Examples

### Example 1:
```
Input
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
Output
[null, 4, 5, 5, 8, 8]

Explanation
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);   // return 4
kthLargest.add(5);   // return 5
kthLargest.add(10);  // return 5
kthLargest.add(9);   // return 8
kthLargest.add(4);   // return 8
```

## Constraints

- `1 <= k <= 10^4`
- `0 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `-10^4 <= val <= 10^4`
- At most `10^4` calls will be made to `add`.

## Solution Approaches

### Approach 1: Min Heap
**Time Complexity:** O(n log k) for constructor, O(log k) for add  
**Space Complexity:** O(k)

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        
        for num in nums:
            self.add(num)
    
    def add(self, val):
        heapq.heappush(self.heap, val)
        
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        
        return self.heap[0]
```

### Approach 2: Min Heap with Heapify
**Time Complexity:** O(n) for constructor, O(log k) for add  
**Space Complexity:** O(k)

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        
        while len(self.heap) > k:
            heapq.heappop(self.heap)
    
    def add(self, val):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            heapq.heapreplace(self.heap, val)
        
        return self.heap[0]
```

### Approach 3: Sorted List (Not Optimal)
**Time Complexity:** O(n log n) for add  
**Space Complexity:** O(n)

```python
import bisect

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.sorted_nums = sorted(nums)
    
    def add(self, val):
        bisect.insort(self.sorted_nums, val)
        return self.sorted_nums[-self.k]
```

## Key Insights

1. **Min heap of size k** keeps k largest elements
2. **Root is kth largest** element
3. **Pop smallest** when heap exceeds size k

## Related Problems

- Kth Largest Element in an Array (LeetCode #215)
- Top K Frequent Elements (LeetCode #347)