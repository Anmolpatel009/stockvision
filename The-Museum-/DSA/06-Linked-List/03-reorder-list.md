# Reorder List

**Difficulty:** Medium  
**Pattern:** Linked List  
**LeetCode:** #143

## Problem Statement

You are given the head of a singly linked-list. The list can be represented as:

`L0 → L1 → … → Ln - 1 → Ln`

Reorder the list to be on the following form:

`L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …`

You may not modify the values in the list's nodes. Only nodes themselves may be changed.

## Examples

### Example 1:
```
Input: head = [1,2,3,4]
Output: [1,4,2,3]
```

### Example 2:
```
Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]
```

## Constraints

- The number of nodes in the list is in the range `[1, 5 * 10^4]`.
- `1 <= Node.val <= 1000`

## Solution Approaches

### Approach 1: Find Middle, Reverse, Merge
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def reorderList(head):
    if not head or not head.next:
        return
    
    # Find middle
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    current = slow.next
    slow.next = None
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    # Merge two halves
    first, second = head, prev
    while second:
        temp1, temp2 = first.next, second.next
        first.next = second
        second.next = temp1
        first, second = temp1, temp2
```

### Approach 2: Using Array
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def reorderList(head):
    if not head:
        return
    
    # Store nodes in array
    nodes = []
    current = head
    while current:
        nodes.append(current)
        current = current.next
    
    # Reorder using two pointers
    left, right = 0, len(nodes) - 1
    while left < right:
        nodes[left].next = nodes[right]
        left += 1
        if left < right:
            nodes[right].next = nodes[left]
            right -= 1
    
    nodes[left].next = None
```

### Approach 3: Recursive
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def reorderList(head):
    def get_length(node):
        length = 0
        while node:
            length += 1
            node = node.next
        return length
    
    def reorder(node, length):
        if length == 0:
            return None
        if length == 1:
            temp = node.next
            node.next = None
            return temp
        if length == 2:
            temp = node.next.next
            node.next.next = None
            return temp
        
        tail = reorder(node.next, length - 2)
        next_node = node.next
        node.next = tail
        tail_next = tail.next
        tail.next = next_node
        
        return tail_next
    
    reorder(head, get_length(head))
```

## Key Insights

1. **Three steps**: Find middle, reverse second half, merge alternately
2. **Slow-fast pointer** to find middle
3. **In-place merge** saves space

## Related Problems

- Reverse Linked List II (LeetCode #92)
- Rotate List (LeetCode #61)