# Subtree of Another Tree

**Difficulty:** Easy  
**Pattern:** Trees  
**LeetCode:** #572

## Problem Statement

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

A subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants.

## Examples

### Example 1:
```
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true
```

### Example 2:
```
Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false
```

## Constraints

- The number of nodes in the `root` tree is in the range `[1, 2000]`.
- The number of nodes in the `subRoot` tree is in the range `[1, 1000]`.
- `-10^4 <= root.val <= 10^4`
- `-10^4 <= subRoot.val <= 10^4`

## Solution Approaches

### Approach 1: Recursive
**Time Complexity:** O(m * n)  
**Space Complexity:** O(h)

```python
def isSubtree(root, subRoot):
    if not root:
        return False
    if not subRoot:
        return True
    
    if isSameTree(root, subRoot):
        return True
    
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)

def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Approach 2: String Matching (Serialize)
**Time Complexity:** O(m + n)  
**Space Complexity:** O(m + n)

```python
def isSubtree(root, subRoot):
    def serialize(node):
        if not node:
            return "#null"
        return "#" + str(node.val) + serialize(node.left) + serialize(node.right)
    
    root_str = serialize(root)
    sub_str = serialize(subRoot)
    
    return sub_str in root_str
```

### Approach 3: Merkle Tree Hashing
**Time Complexity:** O(m + n)  
**Space Complexity:** O(m + n)

```python
import hashlib

def isSubtree(root, subRoot):
    def hash_node(node):
        if not node:
            return "#"
        left_hash = hash_node(node.left)
        right_hash = hash_node(node.right)
        node_hash = hashlib.md5((str(node.val) + left_hash + right_hash).encode()).hexdigest()
        node.hash = node_hash
        return node_hash
    
    def check_subtree(node, sub):
        if not node:
            return False
        if node.hash == sub.hash:
            return isSameTree(node, sub)
        return check_subtree(node.left, sub) or check_subtree(node.right, sub)
    
    hash_node(root)
    hash_node(subRoot)
    
    return check_subtree(root, subRoot)
```

## Key Insights

1. **Check each node** as potential root of subtree
2. **Use isSameTree** helper function
3. **Serialization** enables string matching

## Related Problems

- Same Tree (LeetCode #100)
- Count Univalue Subtrees (LeetCode #250)
- Most Frequent Subtree Sum (LeetCode #508)