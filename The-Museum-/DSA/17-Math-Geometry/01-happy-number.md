# Happy Number

**Difficulty:** Easy  
**Pattern:** Math & Geometry  
**LeetCode:** #202

## Problem Statement
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits.

## Solution Approaches

### Approach 1: Hash Set
**Time Complexity:** O(log n)  
**Space Complexity:** O(log n)

```python
def isHappy(n):
    seen = set()
    
    while n != 1:
        if n in seen:
            return False
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    
    return True
```

### Approach 2: Floyd's Cycle Detection
**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

```python
def isHappy(n):
    def get_next(num):
        total = 0
        while num > 0:
            digit = num % 10
            total += digit ** 2
            num //= 10
        return total
    
    slow = n
    fast = get_next(n)
    
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
    
    return fast == 1
```
