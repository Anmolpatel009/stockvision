# Pacific Atlantic Water Flow

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #417

## Problem Statement

There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. Return a list of grid coordinates where water can flow to both oceans.

## Solution Approaches

### Approach 1: DFS from Oceans
**Time Complexity:** O(m * n)  
**Space Complexity:** O(m * n)

```python
def pacificAtlantic(heights):
    if not heights:
        return []
    
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(i, j, visited, prev_height):
        if (i < 0 or i >= m or j < 0 or j >= n or
            (i, j) in visited or heights[i][j] < prev_height):
            return
        visited.add((i, j))
        dfs(i+1, j, visited, heights[i][j])
        dfs(i-1, j, visited, heights[i][j])
        dfs(i, j+1, visited, heights[i][j])
        dfs(i, j-1, visited, heights[i][j])
    
    for i in range(m):
        dfs(i, 0, pacific, -1)
        dfs(i, n-1, atlantic, -1)
    
    for j in range(n):
        dfs(0, j, pacific, -1)
        dfs(m-1, j, atlantic, -1)
    
    return list(pacific & atlantic)
```

## Key Insights

1. **Start from oceans** and go uphill
2. **Find intersection** of reachable cells from both oceans
