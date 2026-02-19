# Path with Maximum Probability

**Difficulty:** Medium  
**Pattern:** Advanced Graphs  
**LeetCode:** #1514

## Problem Statement
Find the path with maximum probability of success.

## Solution Approaches

### Approach 1: Dijkstra's (Modified for Max)
**Time Complexity:** O(E log V)  
**Space Complexity:** O(V + E)

```python
import heapq

def maxProbability(n, edges, succProb, start, end):
    graph = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, succProb[i]))
        graph[v].append((u, succProb[i]))
    
    probs = [0.0] * n
    probs[start] = 1.0
    
    heap = [(-1.0, start)]
    
    while heap:
        prob, node = heapq.heappop(heap)
        prob = -prob
        
        if node == end:
            return prob
        
        for neighbor, edge_prob in graph[node]:
            new_prob = prob * edge_prob
            if new_prob > probs[neighbor]:
                probs[neighbor] = new_prob
                heapq.heappush(heap, (-new_prob, neighbor))
    
    return probs[end]
```
