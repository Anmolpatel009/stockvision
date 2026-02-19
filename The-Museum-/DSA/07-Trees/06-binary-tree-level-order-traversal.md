# Binary Tree Level Order Traversal

**Difficulty:** Medium  
**Pattern:** Trees  
**LeetCode:** #102

## Problem Statement

Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

## Examples

### Example 1:
```
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

### Example 2:
```
Input: root = [1]
Output: [[1]]
```

### Example 3:
```
Input: root = []
Output: []
```

## Constraints

- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

## Solution Approaches

### Approach 1: BFS with Queue
**Time Complexity:** O(n)  
**Space Complexity:** O(w)

```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### Approach 2: DFS with Level Tracking
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def levelOrder(root):
    result = []
    
    def dfs(node, level):
        if not node:
            return
        
        if len(result) == level:
            result.append([])
        
        result[level].append(node.val)
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)
    
    dfs(root, 0)
    return result
```

### Approach 3: Iterative with Two Arrays
**Time Complexity:** O(n)  
**Space Complexity:** O(w)

```python
def levelOrder(root):
    if not root:
        return []
    
    result = []
    current_level = [root]
    
    while current_level:
        result.append([node.val for node in current_level])
        next_level = []
        
        for node in current_level:
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
        
        current_level = next_level
    
    return result
```

## Key Insights

1. **BFS naturally processes level by level**
2. **Track level size** before processing each level
3. **DFS can also work** with level parameter

## Related Problems

- Binary Tree Zigzag Level Order Traversal (LeetCode #103)
- Binary Tree Right Side View (LeetCode #199)
- Average of Levels in Binary Tree (LeetCode #637)