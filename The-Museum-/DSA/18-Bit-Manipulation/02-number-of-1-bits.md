# Number of 1 Bits

**Difficulty:** Easy  
**Pattern:** Bit Manipulation  
**LeetCode:** #191

## Problem Statement
Write a function that takes the binary representation of an unsigned integer and returns the number of '1' bits.

## Solution Approaches

### Approach 1: Brian Kernighan's Algorithm
**Time Complexity:** O(k) where k is number of 1 bits  
**Space Complexity:** O(1)

```python
def hammingWeight(n):
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count
```

### Approach 2: Built-in
```python
def hammingWeight(n):
    return bin(n).count('1')
```
