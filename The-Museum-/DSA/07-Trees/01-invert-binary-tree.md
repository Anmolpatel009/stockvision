# Invert Binary Tree

**Difficulty:** Easy  
**Pattern:** Trees  
**LeetCode:** #226

## Problem Statement

Given the `root` of a binary tree, invert the tree, and return its root.

## Examples

### Example 1:
```
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

### Example 2:
```
Input: root = [2,1,3]
Output: [2,3,1]
```

### Example 3:
```
Input: root = []
Output: []
```

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

## Solution Approaches

### Approach 1: Recursive DFS
**Time Complexity:** O(n)  
**Space Complexity:** O(h) where h is height

```python
def invertTree(root):
    if not root:
        return None
    
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    
    return root
```

### Approach 2: Iterative BFS
**Time Complexity:** O(n)  
**Space Complexity:** O(w) where w is max width

```python
from collections import deque

def invertTree(root):
    if not root:
        return None
    
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return root
```

### Approach 3: Iterative DFS with Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def invertTree(root):
    if not root:
        return None
    
    stack = [root]
    
    while stack:
        node = stack.pop()
        node.left, node.right = node.right, node.left
        
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return root
```

## Key Insights

1. **Swap left and right** children at each node
2. **Any traversal works** - preorder, postorder, or level order
3. **Base case** is when node is None

## Related Problems

- Symmetric Tree (LeetCode #101)
- Same Tree (LeetCode #100)
- Maximum Depth of Binary Tree (LeetCode #104)