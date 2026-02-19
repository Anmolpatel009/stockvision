# Maximum Depth of Binary Tree

**Difficulty:** Easy  
**Pattern:** Trees  
**LeetCode:** #104

## Problem Statement

Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

## Examples

### Example 1:
```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

### Example 2:
```
Input: root = [1,null,2]
Output: 2
```

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

## Solution Approaches

### Approach 1: Recursive DFS
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def maxDepth(root):
    if not root:
        return 0
    
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Approach 2: Iterative BFS
**Time Complexity:** O(n)  
**Space Complexity:** O(w)

```python
from collections import deque

def maxDepth(root):
    if not root:
        return 0
    
    queue = deque([root])
    depth = 0
    
    while queue:
        depth += 1
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth
```

### Approach 3: Iterative DFS with Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def maxDepth(root):
    if not root:
        return 0
    
    stack = [(root, 1)]
    max_depth = 0
    
    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    
    return max_depth
```

## Key Insights

1. **Depth = 1 + max(left_depth, right_depth)**
2. **BFS counts levels** naturally
3. **DFS tracks depth** with each node

## Related Problems

- Minimum Depth of Binary Tree (LeetCode #111)
- Balanced Binary Tree (LeetCode #110)
- Maximum Depth of N-ary Tree (LeetCode #559)