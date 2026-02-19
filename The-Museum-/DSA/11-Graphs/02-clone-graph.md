# Clone Graph

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #133

## Problem Statement

Given a reference of a node in a connected undirected graph, return a deep copy of the graph.

## Solution Approaches

### Approach 1: DFS with Hash Map
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

```python
def cloneGraph(node):
    if not node:
        return None
    
    visited = {}
    
    def dfs(n):
        if n in visited:
            return visited[n]
        
        clone = Node(n.val)
        visited[n] = clone
        
        for neighbor in n.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

### Approach 2: BFS
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V)

```python
from collections import deque

def cloneGraph(node):
    if not node:
        return None
    
    visited = {node: Node(node.val)}
    queue = deque([node])
    
    while queue:
        n = queue.popleft()
        for neighbor in n.neighbors:
            if neighbor not in visited:
                visited[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            visited[n].neighbors.append(visited[neighbor])
    
    return visited[node]
```

## Key Insights

1. **Hash map** maps original nodes to clones
2. **DFS/BFS** traverses graph and creates copies
3. **Handle neighbors** by looking up or creating clones

## Related Problems

- Copy List with Random Pointer (LeetCode #138)
