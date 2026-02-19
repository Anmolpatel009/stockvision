# Construct Binary Tree from Preorder and Inorder Traversal

**Difficulty:** Medium  
**Pattern:** Trees  
**LeetCode:** #105

## Problem Statement

Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

## Examples

### Example 1:
```
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

### Example 2:
```
Input: preorder = [-1], inorder = [-1]
Output: [-1]
```

## Constraints

- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- `preorder` and `inorder` consist of unique values.
- Each value of `inorder` also appears in `preorder`.
- `preorder` is guaranteed to be the preorder traversal of a binary tree.
- `inorder` is guaranteed to be the inorder traversal of the same binary tree.

## Solution Approaches

### Approach 1: Recursive with Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def buildTree(preorder, inorder):
    inorder_map = {val: i for i, val in enumerate(inorder)}
    preorder_idx = [0]
    
    def build(left, right):
        if left > right:
            return None
        
        root_val = preorder[preorder_idx[0]]
        preorder_idx[0] += 1
        root = TreeNode(root_val)
        
        root.left = build(left, inorder_map[root_val] - 1)
        root.right = build(inorder_map[root_val] + 1, right)
        
        return root
    
    return build(0, len(inorder) - 1)
```

### Approach 2: Recursive with Array Slicing
**Time Complexity:** O(n²)  
**Space Complexity:** O(n²)

```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    mid = inorder.index(root_val)
    
    root.left = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:], inorder[mid+1:])
    
    return root
```

### Approach 3: Iterative with Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def buildTree(preorder, inorder):
    if not preorder:
        return None
    
    root = TreeNode(preorder[0])
    stack = [root]
    inorder_idx = 0
    
    for i in range(1, len(preorder)):
        node = TreeNode(preorder[i])
        
        if stack[-1].val != inorder[inorder_idx]:
            stack[-1].left = node
        else:
            while stack and stack[-1].val == inorder[inorder_idx]:
                parent = stack.pop()
                inorder_idx += 1
            parent.right = node
        
        stack.append(node)
    
    return root
```

## Key Insights

1. **First element in preorder** is always the root
2. **Find root in inorder** to split left/right subtrees
3. **Use hash map** for O(1) lookup of inorder indices

## Related Problems

- Construct Binary Tree from Inorder and Postorder Traversal (LeetCode #106)
- Construct Binary Search Tree from Preorder Traversal (LeetCode #1008)