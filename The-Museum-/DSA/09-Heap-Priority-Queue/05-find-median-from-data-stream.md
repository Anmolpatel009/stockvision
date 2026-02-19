# Find Median from Data Stream

**Difficulty:** Hard  
**Pattern:** Heap / Priority Queue  
**LeetCode:** #295

## Problem Statement

The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

Implement the MedianFinder class:
- `MedianFinder()` initializes the MedianFinder object.
- `void addNum(int num)` adds the integer num from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far.

## Examples

### Example 1:
```
Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output
[null, null, null, 1.5, null, 2.0]
```

## Constraints

- `-10^5 <= num <= 10^5`
- There will be at least one element in the data structure before calling findMedian.
- At most `5 * 10^4` calls will be made to addNum and findMedian.

## Solution Approaches

### Approach 1: Two Heaps
**Time Complexity:** O(log n) for addNum, O(1) for findMedian  
**Space Complexity:** O(n)

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negated values)
        self.large = []  # Min heap
    
    def addNum(self, num):
        # Push to max heap, then pop max to min heap
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Balance: small should have >= elements than large
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

### Approach 2: Two Heaps with Lazy Removal
**Time Complexity:** O(log n) amortized  
**Space Complexity:** O(n)

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap
        self.large = []  # Min heap
        self.small_size = 0
        self.large_size = 0
    
    def addNum(self, num):
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.small_size += 1
        else:
            heapq.heappush(self.large, num)
            self.large_size += 1
        
        # Rebalance
        if self.small_size > self.large_size + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
            self.small_size -= 1
            self.large_size += 1
        elif self.large_size > self.small_size:
            heapq.heappush(self.small, -heapq.heappop(self.large))
            self.large_size -= 1
            self.small_size += 1
    
    def findMedian(self):
        if self.small_size > self.large_size:
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

### Approach 3: Sorted List (Not Optimal)
**Time Complexity:** O(n) for addNum, O(1) for findMedian  
**Space Complexity:** O(n)

```python
import bisect

class MedianFinder:
    def __init__(self):
        self.nums = []
    
    def addNum(self, num):
        bisect.insort(self.nums, num)
    
    def findMedian(self):
        n = len(self.nums)
        if n % 2 == 1:
            return self.nums[n // 2]
        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2
```

## Key Insights

1. **Two heaps**: max heap for smaller half, min heap for larger half
2. **Balance heaps** so sizes differ by at most 1
3. **Median is** top of larger heap or average of both tops

## Related Problems

- Sliding Window Median (LeetCode #480)
- IPO (LeetCode #502)