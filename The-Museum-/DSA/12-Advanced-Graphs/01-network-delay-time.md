# Network Delay Time

**Difficulty:** Medium  
**Pattern:** Advanced Graphs  
**LeetCode:** #743

## Problem Statement
You are given a network of n nodes, labeled from 1 to n. Return the minimum time it takes for a signal to reach all nodes.

## Solution Approaches

### Approach 1: Dijkstra's Algorithm
**Time Complexity:** O(E log V)  
**Space Complexity:** O(V + E)

```python
import heapq
from collections import defaultdict

def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    distances = {i: float('inf') for i in range(1, n + 1)}
    distances[k] = 0
    
    heap = [(0, k)]
    visited = set()
    
    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    max_dist = max(distances.values())
    return max_dist if max_dist != float('inf') else -1
```
