# Copy List with Random Pointer

**Difficulty:** Medium  
**Pattern:** Linked List  
**LeetCode:** #138

## Problem Statement

A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.

Construct a deep copy of the list. The deep copy should consist of exactly `n` brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointer of the new nodes should point to new nodes in the copied list.

## Examples

### Example 1:
```
Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
```

### Example 2:
```
Input: head = [[1,1],[2,1]]
Output: [[1,1],[2,1]]
```

## Constraints

- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
- `Node.random` is `null` or is pointing to some node in the linked list.

## Solution Approaches

### Approach 1: Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def copyRandomList(head):
    if not head:
        return None
    
    # Create mapping from old to new nodes
    old_to_new = {}
    current = head
    
    # First pass: create all new nodes
    while current:
        old_to_new[current] = Node(current.val)
        current = current.next
    
    # Second pass: set next and random pointers
    current = head
    while current:
        if current.next:
            old_to_new[current].next = old_to_new[current.next]
        if current.random:
            old_to_new[current].random = old_to_new[current.random]
        current = current.next
    
    return old_to_new[head]
```

### Approach 2: Interweaving Nodes
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def copyRandomList(head):
    if not head:
        return None
    
    # Step 1: Create interweaved list
    current = head
    while current:
        new_node = Node(current.val)
        new_node.next = current.next
        current.next = new_node
        current = new_node.next
    
    # Step 2: Set random pointers
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next
    
    # Step 3: Separate the lists
    current = head
    new_head = head.next
    while current:
        new_node = current.next
        current.next = new_node.next
        if new_node.next:
            new_node.next = new_node.next.next
        current = current.next
    
    return new_head
```

### Approach 3: Recursive with Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def copyRandomList(head):
    visited = {}
    
    def clone(node):
        if not node:
            return None
        
        if node in visited:
            return visited[node]
        
        new_node = Node(node.val)
        visited[node] = new_node
        
        new_node.next = clone(node.next)
        new_node.random = clone(node.random)
        
        return new_node
    
    return clone(head)
```

## Key Insights

1. **Two-pass approach** - create nodes first, then set pointers
2. **Hash map** maps original nodes to copies
3. **Interweaving** achieves O(1) space

## Related Problems

- Clone Graph (LeetCode #133)
- Copy List with Random Pointer (LeetCode #138)