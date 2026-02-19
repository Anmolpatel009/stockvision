# Koko Eating Bananas

**Difficulty:** Medium  
**Pattern:** Binary Search  
**LeetCode:** #875

## Problem Statement

Koko loves to eat bananas. There are `n` piles of bananas, the `i`th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.

Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

## Examples

### Example 1:
```
Input: piles = [3,6,7,11], h = 8
Output: 4
```

### Example 2:
```
Input: piles = [30,11,23,4,20], h = 5
Output: 30
```

### Example 3:
```
Input: piles = [30,11,23,4,20], h = 6
Output: 23
```

## Constraints

- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`

## Solution Approaches

### Approach 1: Binary Search on Answer
**Time Complexity:** O(n log m) where m is max pile  
**Space Complexity:** O(1)

```python
import math

def minEatingSpeed(piles, h):
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        hours = sum(math.ceil(pile / mid) for pile in piles)
        
        if hours <= h:
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Approach 2: Binary Search with Helper Function
**Time Complexity:** O(n log m)  
**Space Complexity:** O(1)

```python
import math

def minEatingSpeed(piles, h):
    def can_finish(k):
        return sum(math.ceil(pile / k) for pile in piles) <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Approach 3: Optimized with Integer Division
**Time Complexity:** O(n log m)  
**Space Complexity:** O(1)

```python
def minEatingSpeed(piles, h):
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        hours = sum((pile + mid - 1) // mid for pile in piles)
        
        if hours <= h:
            right = mid
        else:
            left = mid + 1
    
    return left
```

## Key Insights

1. **Binary search on answer** - search for minimum k
2. **Search space**: 1 to max(piles)
3. **Calculate hours** needed for each k value

## Related Problems

- Capacity To Ship Packages Within D Days (LeetCode #1011)
- Minimum Number of Days to Make m Bouquets (LeetCode #1482)