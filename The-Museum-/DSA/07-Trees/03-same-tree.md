# Same Tree

**Difficulty:** Easy  
**Pattern:** Trees  
**LeetCode:** #100

## Problem Statement

Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

## Examples

### Example 1:
```
Input: p = [1,2,3], q = [1,2,3]
Output: true
```

### Example 2:
```
Input: p = [1,2], q = [1,null,2]
Output: false
```

### Example 3:
```
Input: p = [1,2,1], q = [1,1,2]
Output: false
```

## Constraints

- The number of nodes in both trees is in the range `[0, 100]`.
- `-10^4 <= Node.val <= 10^4`

## Solution Approaches

### Approach 1: Recursive DFS
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Approach 2: Iterative BFS
**Time Complexity:** O(n)  
**Space Complexity:** O(w)

```python
from collections import deque

def isSameTree(p, q):
    queue = deque([(p, q)])
    
    while queue:
        node1, node2 = queue.popleft()
        
        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False
        
        queue.append((node1.left, node2.left))
        queue.append((node1.right, node2.right))
    
    return True
```

### Approach 3: Iterative DFS with Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def isSameTree(p, q):
    stack = [(p, q)]
    
    while stack:
        node1, node2 = stack.pop()
        
        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False
        
        stack.append((node1.left, node2.left))
        stack.append((node1.right, node2.right))
    
    return True
```

## Key Insights

1. **Both None** means same (base case)
2. **One None** means different
3. **Values must match** and subtrees must be same

## Related Problems

- Symmetric Tree (LeetCode #101)
- Subtree of Another Tree (LeetCode #572)
- Merge Two Binary Trees (LeetCode #617)