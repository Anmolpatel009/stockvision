# Insert Interval

**Difficulty:** Medium  
**Pattern:** Intervals  
**LeetCode:** #57

## Problem Statement
Insert newInterval into intervals and merge if necessary.

## Solution Approaches

### Approach 1: Three Phase
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def insert(intervals, newInterval):
    result = []
    i = 0
    
    # Add all intervals before newInterval
    while i < len(intervals) and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    
    # Add remaining intervals
    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    
    return result
```
