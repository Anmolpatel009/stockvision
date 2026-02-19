# Reverse Bits

**Difficulty:** Easy  
**Pattern:** Bit Manipulation  
**LeetCode:** #190

## Problem Statement
Reverse bits of a given 32 bits unsigned integer.

## Solution Approaches

### Approach 1: Bit by Bit
**Time Complexity:** O(32) = O(1)  
**Space Complexity:** O(1)

```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```
