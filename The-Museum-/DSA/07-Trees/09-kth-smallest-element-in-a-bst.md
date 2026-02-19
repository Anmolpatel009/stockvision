# Kth Smallest Element in a BST

**Difficulty:** Medium  
**Pattern:** Trees  
**LeetCode:** #230

## Problem Statement

Given the `root` of a binary search tree, and an integer `k`, return the `k`th smallest value (1-indexed) in the tree.

## Examples

### Example 1:
```
Input: root = [3,1,4,null,2], k = 1
Output: 1
```

### Example 2:
```
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
```

## Constraints

- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

## Solution Approaches

### Approach 1: Inorder Traversal (Recursive)
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def kthSmallest(root, k):
    result = []
    
    def inorder(node):
        if not node or len(result) >= k:
            return
        
        inorder(node.left)
        if len(result) < k:
            result.append(node.val)
        inorder(node.right)
    
    inorder(root)
    return result[-1]
```

### Approach 2: Inorder Traversal (Iterative)
**Time Complexity:** O(h + k)  
**Space Complexity:** O(h)

```python
def kthSmallest(root, k):
    stack = []
    current = root
    
    while True:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        k -= 1
        
        if k == 0:
            return current.val
        
        current = current.right
```

### Approach 3: Morris Traversal
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def kthSmallest(root, k):
    current = root
    
    while current:
        if not current.left:
            k -= 1
            if k == 0:
                return current.val
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                k -= 1
                if k == 0:
                    return current.val
                current = current.right
    
    return -1
```

## Key Insights

1. **Inorder traversal of BST** gives sorted order
2. **Stop early** when kth element found
3. **Iterative approach** allows early termination

## Related Problems

- Validate Binary Search Tree (LeetCode #98)
- Binary Tree Inorder Traversal (LeetCode #94)
- Closest Binary Search Tree Value (LeetCode #270)