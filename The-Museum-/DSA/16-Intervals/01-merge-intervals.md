# Merge Intervals

**Difficulty:** Medium  
**Pattern:** Intervals  
**LeetCode:** #56

## Problem Statement
Given an array of intervals, merge all overlapping intervals.

## Solution Approaches

### Approach 1: Sort and Merge
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def merge(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]
    
    for interval in intervals[1:]:
        if interval[0] <= result[-1][1]:
            result[-1][1] = max(result[-1][1], interval[1])
        else:
            result.append(interval)
    
    return result
```
