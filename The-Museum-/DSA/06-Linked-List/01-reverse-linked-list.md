# Reverse Linked List

**Difficulty:** Easy  
**Pattern:** Linked List  
**LeetCode:** #206

## Problem Statement

Given the `head` of a singly linked list, reverse the list, and return the reversed list.

## Examples

### Example 1:
```
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

### Example 2:
```
Input: head = [1,2]
Output: [2,1]
```

### Example 3:
```
Input: head = []
Output: []
```

## Constraints

- The number of nodes in the list is the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

## Solution Approaches

### Approach 1: Iterative
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def reverseList(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev
```

### Approach 2: Recursive
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def reverseList(head):
    if not head or not head.next:
        return head
    
    new_head = reverseList(head.next)
    head.next.next = head
    head.next = None
    
    return new_head
```

### Approach 3: Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def reverseList(head):
    if not head:
        return None
    
    stack = []
    current = head
    
    while current:
        stack.append(current)
        current = current.next
    
    new_head = stack.pop()
    current = new_head
    
    while stack:
        current.next = stack.pop()
        current = current.next
    
    current.next = None
    return new_head
```

## Key Insights

1. **Iterative approach** uses three pointers: prev, current, next
2. **Recursive approach** reverses rest of list then fixes current node
3. **Always set last node's next to None**

## Related Problems

- Reverse Linked List II (LeetCode #92)
- Reverse Nodes in k-Group (LeetCode #25)
- Palindrome Linked List (LeetCode #234)