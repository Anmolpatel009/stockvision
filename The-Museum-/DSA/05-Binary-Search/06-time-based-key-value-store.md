# Time Based Key-Value Store

**Difficulty:** Medium  
**Pattern:** Binary Search  
**LeetCode:** #981

## Problem Statement

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the `TimeMap` class:
- `TimeMap()` Initializes the object.
- `void set(String key, String value, int timestamp)` Stores the key with the value at the given timestamp.
- `String get(String key, int timestamp)` Returns the most recent value of the key if set was previously called on it and the most recent timestamp for that key is less than or equal to timestamp. If there are no values, it returns `""`.

## Examples

### Example 1:
```
Input: ["TimeMap", "set", ["foo", "bar", 1], "get", ["foo", 1], "get", ["foo", 3], "set", ["foo", "bar2", 4], "get", ["foo", 4], "get", ["foo", 5]]
Output: [null, null, "bar", "bar", null, "bar2", "bar2"]
```

## Constraints

- `1 <= key.length, value.length <= 100`
- `key` and `value` consist of lowercase English letters and digits.
- `1 <= timestamp <= 10^7`
- All the timestamps timestamp of set are strictly increasing.
- At most `2 * 10^5` calls will be made to set and get.

## Solution Approaches

### Approach 1: Binary Search on Sorted List
**Time Complexity:** O(log n) for get, O(1) for set  
**Space Complexity:** O(n)

```python
class TimeMap:
    def __init__(self):
        self.store = {}  # key: list of (timestamp, value)
    
    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))
    
    def get(self, key, timestamp):
        if key not in self.store:
            return ""
        
        entries = self.store[key]
        left, right = 0, len(entries) - 1
        result = ""
        
        while left <= right:
            mid = (left + right) // 2
            if entries[mid][0] <= timestamp:
                result = entries[mid][1]
                left = mid + 1
            else:
                right = mid - 1
        
        return result
```

### Approach 2: Using Bisect
**Time Complexity:** O(log n) for get, O(1) for set  
**Space Complexity:** O(n)

```python
import bisect

class TimeMap:
    def __init__(self):
        self.store = {}
    
    def set(self, key, value, timestamp):
        if key not in self.store:
            self.store[key] = {'times': [], 'values': []}
        self.store[key]['times'].append(timestamp)
        self.store[key]['values'].append(value)
    
    def get(self, key, timestamp):
        if key not in self.store:
            return ""
        
        times = self.store[key]['times']
        values = self.store[key]['values']
        
        idx = bisect.bisect_right(times, timestamp) - 1
        
        if idx >= 0:
            return values[idx]
        return ""
```

### Approach 3: Separate Times and Values
**Time Complexity:** O(log n) for get, O(1) for set  
**Space Complexity:** O(n)

```python
class TimeMap:
    def __init__(self):
        self.key_time = {}  # key -> list of timestamps
        self.key_value = {}  # key -> list of values
    
    def set(self, key, value, timestamp):
        if key not in self.key_time:
            self.key_time[key] = []
            self.key_value[key] = []
        self.key_time[key].append(timestamp)
        self.key_value[key].append(value)
    
    def get(self, key, timestamp):
        if key not in self.key_time:
            return ""
        
        times = self.key_time[key]
        values = self.key_value[key]
        
        left, right = 0, len(times)
        
        while left < right:
            mid = (left + right) // 2
            if times[mid] <= timestamp:
                left = mid + 1
            else:
                right = mid
        
        return values[left - 1] if left > 0 else ""
```

## Key Insights

1. **Timestamps are strictly increasing** - no need to sort
2. **Binary search for largest timestamp <= target**
3. **Store as list of tuples** or separate lists

## Related Problems

- Snapshot Array (LeetCode #1146)
- Range Module (LeetCode #715)