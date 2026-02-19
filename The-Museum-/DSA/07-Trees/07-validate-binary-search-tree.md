# Validate Binary Search Tree

**Difficulty:** Medium  
**Pattern:** Trees  
**LeetCode:** #98

## Problem Statement

Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

## Examples

### Example 1:
```
Input: root = [2,1,3]
Output: true
```

### Example 2:
```
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.
```

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

## Solution Approaches

### Approach 1: Recursive with Range
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def isValidBST(root):
    def validate(node, low, high):
        if not node:
            return True
        
        if node.val <= low or node.val >= high:
            return False
        
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    
    return validate(root, float('-inf'), float('inf'))
```

### Approach 2: Inorder Traversal
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def isValidBST(root):
    prev = float('-inf')
    stack = []
    current = root
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        
        if current.val <= prev:
            return False
        prev = current.val
        
        current = current.right
    
    return True
```

### Approach 3: Recursive Inorder
**Time Complexity:** O(n)  
**Space Complexity:** O(h)

```python
def isValidBST(root):
    prev = [float('-inf')]
    
    def inorder(node):
        if not node:
            return True
        
        if not inorder(node.left):
            return False
        
        if node.val <= prev[0]:
            return False
        prev[0] = node.val
        
        return inorder(node.right)
    
    return inorder(root)
```

## Key Insights

1. **BST property**: left < root < right for ALL nodes
2. **Track valid range** as you traverse
3. **Inorder traversal** of BST is sorted

## Related Problems

- Binary Tree Inorder Traversal (LeetCode #94)
- Convert Sorted Array to Binary Search Tree (LeetCode #108)
- Find Mode in Binary Search Tree (LeetCode #501)