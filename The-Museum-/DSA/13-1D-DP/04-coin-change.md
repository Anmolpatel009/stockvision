# Coin Change

**Difficulty:** Medium  
**Pattern:** 1D Dynamic Programming  
**LeetCode:** #322

## Problem Statement
Return the fewest number of coins that you need to make up that amount. If not possible, return -1.

## Solution Approaches

### Approach 1: DP
**Time Complexity:** O(amount * n_coins)  
**Space Complexity:** O(amount)

```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Approach 2: BFS
```python
from collections import deque

def coinChange(coins, amount):
    if amount == 0:
        return 0
    
    queue = deque([(0, 0)])
    visited = set()
    
    while queue:
        curr, steps = queue.popleft()
        for coin in coins:
            next_val = curr + coin
            if next_val == amount:
                return steps + 1
            if next_val < amount and next_val not in visited:
                visited.add(next_val)
                queue.append((next_val, steps + 1))
    
    return -1
```
