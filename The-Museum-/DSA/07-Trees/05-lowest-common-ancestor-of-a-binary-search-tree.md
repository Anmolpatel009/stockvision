# Lowest Common Ancestor of a Binary Search Tree

**Difficulty:** Medium  
**Pattern:** Trees  
**LeetCode:** #235

## Problem Statement

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in T that has both `p` and `q` as descendants.

## Examples

### Example 1:
```
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
Explanation: The LCA of nodes 2 and 8 is 6.
```

### Example 2:
```
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: The LCA of nodes 2 and 4 is 2.
```

## Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the BST.

## Solution Approaches

### Approach 1: Iterative
**Time Complexity:** O(h)  
**Space Complexity:** O(1)

```python
def lowestCommonAncestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

### Approach 2: Recursive
**Time Complexity:** O(h)  
**Space Complexity:** O(h)

```python
def lowestCommonAncestor(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor(root.left, p, q)
    elif p.val > root.val and q.val > root.val:
        return lowestCommonAncestor(root.right, p, q)
    else:
        return root
```

### Approach 3: Path Comparison
**Time Complexity:** O(h)  
**Space Complexity:** O(h)

```python
def lowestCommonAncestor(root, p, q):
    def find_path(node, target, path):
        if not node:
            return False
        path.append(node)
        if node == target:
            return True
        if (target.val < node.val and find_path(node.left, target, path)) or \
           (target.val > node.val and find_path(node.right, target, path)):
            return True
        path.pop()
        return False
    
    path_p, path_q = [], []
    find_path(root, p, path_p)
    find_path(root, q, path_q)
    
    lca = root
    for i in range(min(len(path_p), len(path_q))):
        if path_p[i] == path_q[i]:
            lca = path_p[i]
        else:
            break
    
    return lca
```

## Key Insights

1. **BST property**: left < root < right
2. **LCA is where paths diverge** - one node on each side
3. **If both smaller**, go left; if both larger, go right

## Related Problems

- Lowest Common Ancestor of a Binary Tree (LeetCode #236)
- Binary Tree Lowest Common Ancestor (LeetCode #1676)