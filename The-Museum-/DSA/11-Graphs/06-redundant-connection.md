# Redundant Connection

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #684

## Problem Statement

In this problem, a tree is an undirected graph that is connected and has no cycles. Return an edge that can be removed so that the resulting graph is a tree.

## Solution Approaches

### Approach 1: Union Find
**Time Complexity:** O(n * alpha(n))  
**Space Complexity:** O(n)

```python
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[px] = py
        return True
    
    for u, v in edges:
        if not union(u, v):
            return [u, v]
    return []
```

## Key Insights

1. **Union Find** detects cycle when both nodes already connected
2. **Return first edge** that creates cycle
