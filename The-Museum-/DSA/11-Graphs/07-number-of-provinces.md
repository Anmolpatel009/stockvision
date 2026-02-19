# Number of Provinces

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #547

## Problem Statement
There are n cities. A province is a group of directly or indirectly connected cities. Return the number of provinces.

## Solution Approaches

### Approach 1: DFS
**Time Complexity:** O(n²)  
**Space Complexity:** O(n)

```python
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = [False] * n
    count = 0
    
    def dfs(city):
        for neighbor in range(n):
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                dfs(neighbor)
    
    for city in range(n):
        if not visited[city]:
            visited[city] = True
            dfs(city)
            count += 1
    return count
```

### Approach 2: Union Find
```python
def findCircleNum(isConnected):
    n = len(isConnected)
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                parent[find(i)] = find(j)
    
    return len(set(find(i) for i in range(n)))
```
