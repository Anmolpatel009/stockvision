# Task Scheduler

**Difficulty:** Medium  
**Pattern:** Heap / Priority Queue  
**LeetCode:** #621

## Problem Statement

Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same letter in the array), that is that there must be at least `n` units of time between any two same tasks.

Return the least number of units of times that the CPU will take to finish all the given tasks.

## Examples

### Example 1:
```
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
```

### Example 2:
```
Input: tasks = ["A","A","A","B","B","B"], n = 0
Output: 6
```

### Example 3:
```
Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
Output: 16
```

## Constraints

- `1 <= tasks.length <= 10^4`
- `tasks[i]` is an uppercase English letter.
- `n` is in the range `[0, 100]`.

## Solution Approaches

### Approach 1: Max Heap
**Time Complexity:** O(n * m) where m is unique tasks  
**Space Complexity:** O(m)

```python
import heapq
from collections import Counter

def leastInterval(tasks, n):
    counts = Counter(tasks)
    max_heap = [-count for count in counts.values()]
    heapq.heapify(max_heap)
    
    time = 0
    while max_heap:
        cycle = n + 1
        store = []
        
        for _ in range(cycle):
            if max_heap:
                count = heapq.heappop(max_heap)
                count += 1
                if count < 0:
                    store.append(count)
                time += 1
            elif store:
                time += 1
        
        for count in store:
            heapq.heappush(max_heap, count)
    
    return time
```

### Approach 2: Mathematical Formula
**Time Complexity:** O(n)  
**Space Complexity:** O(26) = O(1)

```python
from collections import Counter

def leastInterval(tasks, n):
    counts = Counter(tasks)
    max_count = max(counts.values())
    max_count_tasks = sum(1 for count in counts.values() if count == max_count)
    
    # Formula: (max_count - 1) * (n + 1) + max_count_tasks
    result = (max_count - 1) * (n + 1) + max_count_tasks
    
    return max(result, len(tasks))
```

### Approach 3: Greedy with Queue
**Time Complexity:** O(n * m)  
**Space Complexity:** O(m)

```python
from collections import Counter, deque

def leastInterval(tasks, n):
    counts = Counter(tasks)
    max_heap = [-count for count in counts.values()]
    heapq.heapify(max_heap)
    
    queue = deque()  # (count, available_time)
    time = 0
    
    while max_heap or queue:
        time += 1
        
        if max_heap:
            count = heapq.heappop(max_heap) + 1
            if count < 0:
                queue.append((count, time + n))
        
        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])
    
    return time
```

## Key Insights

1. **Most frequent task** determines minimum time
2. **Formula**: (max_count - 1) * (n + 1) + count_of_max
3. **Result is max** of formula and total tasks

## Related Problems

- Rearrange String k Distance Apart (LeetCode #358)
- Distant Barcodes (LeetCode #1054)