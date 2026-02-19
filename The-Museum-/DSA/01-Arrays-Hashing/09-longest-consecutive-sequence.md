# Longest Consecutive Sequence

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #128

## Problem Statement

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

## Examples

### Example 1:
```
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
```

### Example 2:
```
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
```

## Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Solution Approaches

### Approach 1: Hash Set
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def longestConsecutive(nums):
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Only start counting if num is the start of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1
            
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1
            
            longest = max(longest, current_streak)
    
    return longest
```

### Approach 2: Hash Map with Sequence Tracking
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def longestConsecutive(nums):
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in nums:
        # Check if this is the start of a sequence
        if num - 1 not in num_set:
            current = num
            length = 1
            
            while current + 1 in num_set:
                current += 1
                length += 1
            
            max_length = max(max_length, length)
    
    return max_length
```

### Approach 3: Union Find
**Time Complexity:** O(n α(n)) ≈ O(n)  
**Space Complexity:** O(n)

```python
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.size = {}
    
    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
            self.size[py] += self.size[px]

def longestConsecutive(nums):
    if not nums:
        return 0
    
    uf = UnionFind()
    num_set = set(nums)
    
    for num in num_set:
        if num - 1 in num_set:
            uf.union(num, num - 1)
        if num + 1 in num_set:
            uf.union(num, num + 1)
    
    return max(uf.size.values()) if uf.size else 1
```

## Key Insights

1. **Only start counting from sequence starts** - numbers without a predecessor
2. **Hash set** provides O(1) lookups
3. Each number is visited at most twice - O(n) overall

## Related Problems

- Binary Tree Longest Consecutive Sequence (LeetCode #298)
- Longest Consecutive Sequence II (LeetCode #674)
