# Cheapest Flights Within K Stops

**Difficulty:** Medium  
**Pattern:** Advanced Graphs  
**LeetCode:** #787

## Problem Statement
Find the cheapest price from src to dst with at most k stops.

## Solution Approaches

### Approach 1: Bellman-Ford
**Time Complexity:** O(K * E)  
**Space Complexity:** O(n)

```python
def findCheapestPrice(n, flights, src, dst, k):
    prices = [float('inf')] * n
    prices[src] = 0
    
    for _ in range(k + 1):
        temp = prices[:]
        for u, v, w in flights:
            if prices[u] != float('inf'):
                temp[v] = min(temp[v], prices[u] + w)
        prices = temp
    
    return prices[dst] if prices[dst] != float('inf') else -1
```

### Approach 2: BFS with Priority Queue
```python
import heapq

def findCheapestPrice(n, flights, src, dst, k):
    graph = [[] for _ in range(n)]
    for u, v, w in flights:
        graph[u].append((v, w))
    
    heap = [(0, src, 0)]
    visited = {}
    
    while heap:
        cost, city, stops = heapq.heappop(heap)
        if city == dst:
            return cost
        if stops > k:
            continue
        if city in visited and visited[city] <= stops:
            continue
        visited[city] = stops
        
        for neighbor, price in graph[city]:
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))
    
    return -1
```
