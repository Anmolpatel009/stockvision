# Number of Islands

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #200

## Problem Statement

Given an `m x n` 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

## Examples

### Example 1:
```
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
```

### Example 2:
```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is '0' or '1'.

## Solution Approaches

### Approach 1: DFS
**Time Complexity:** O(m * n)  
**Space Complexity:** O(m * n)

```python
def numIslands(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'
        dfs(i+1, j)
        dfs(i-1, j)
        dfs(i, j+1)
        dfs(i, j-1)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    
    return count
```

### Approach 2: BFS
**Time Complexity:** O(m * n)  
**Space Complexity:** O(min(m, n))

```python
from collections import deque

def numIslands(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                queue = deque([(i, j)])
                grid[i][j] = '0'
                
                while queue:
                    r, c = queue.popleft()
                    for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
    
    return count
```

### Approach 3: Union Find
**Time Complexity:** O(m * n * alpha(m*n))  
**Space Complexity:** O(m * n)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = 0
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        return True

def numIslands(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m * n)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                uf.count += 1
                if i > 0 and grid[i-1][j] == '1':
                    uf.union(i*n + j, (i-1)*n + j)
                if j > 0 and grid[i][j-1] == '1':
                    uf.union(i*n + j, i*n + j - 1)
    
    return uf.count
```

## Key Insights

1. **DFS/BFS** marks visited cells by changing '1' to '0'
2. **Count islands** by counting DFS/BFS initiations
3. **Union Find** connects adjacent land cells

## Related Problems

- Surrounded Regions (LeetCode #130)
- Max Area of Island (LeetCode #695)
