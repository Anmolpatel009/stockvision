# Best Time to Buy and Sell Stock

**Difficulty:** Easy  
**Pattern:** Sliding Window  
**LeetCode:** #121

## Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.

## Examples

### Example 1:
```
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
```

### Example 2:
```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: No transactions are done and the max profit = 0.
```

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Solution Approaches

### Approach 1: One Pass
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit
```

### Approach 2: Sliding Window
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def maxProfit(prices):
    left, right = 0, 1
    max_profit = 0
    
    while right < len(prices):
        if prices[left] < prices[right]:
            profit = prices[right] - prices[left]
            max_profit = max(max_profit, profit)
        else:
            left = right
        right += 1
    
    return max_profit
```

### Approach 3: Kadane's Algorithm (Maximum Subarray)
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def maxProfit(prices):
    n = len(prices)
    if n < 2:
        return 0
    
    # Calculate daily changes
    changes = [prices[i+1] - prices[i] for i in range(n-1)]
    
    # Find maximum subarray sum
    max_sum = 0
    current_sum = 0
    
    for change in changes:
        current_sum = max(0, current_sum + change)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

## Key Insights

1. **Track minimum price** as you iterate
2. **Calculate profit** at each step using current price - min_price
3. **Single transaction** means one buy and one sell

## Related Problems

- Best Time to Buy and Sell Stock II (LeetCode #122)
- Best Time to Buy and Sell Stock III (LeetCode #123)
- Best Time to Buy and Sell Stock IV (LeetCode #188)
- Best Time to Buy and Sell Stock with Cooldown (LeetCode #309)