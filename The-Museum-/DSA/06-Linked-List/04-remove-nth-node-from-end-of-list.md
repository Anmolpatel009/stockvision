# Remove Nth Node From End of List

**Difficulty:** Medium  
**Pattern:** Linked List  
**LeetCode:** #19

## Problem Statement

Given the `head` of a linked list, remove the `n`th node from the end of the list and return its head.

## Examples

### Example 1:
```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

### Example 2:
```
Input: head = [1], n = 1
Output: []
```

### Example 3:
```
Input: head = [1,2], n = 1
Output: [1]
```

## Constraints

- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

## Solution Approaches

### Approach 1: Two Pointers
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy
    
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Remove the nth node
    slow.next = slow.next.next
    
    return dummy.next
```

### Approach 2: Two Pass
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def removeNthFromEnd(head, n):
    # First pass: get length
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    
    # Handle edge case
    if n == length:
        return head.next
    
    # Second pass: remove node
    current = head
    for _ in range(length - n - 1):
        current = current.next
    
    current.next = current.next.next
    
    return head
```

### Approach 3: Using Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    stack = []
    current = dummy
    
    while current:
        stack.append(current)
        current = current.next
    
    # Pop n nodes to reach the node before target
    for _ in range(n):
        stack.pop()
    
    prev = stack[-1]
    prev.next = prev.next.next
    
    return dummy.next
```

## Key Insights

1. **Dummy node** handles edge case of removing head
2. **Fast pointer moves n+1 steps** ahead first
3. **Gap of n nodes** between fast and slow pointers

## Related Problems

- Delete Node in a Linked List (LeetCode #237)
- Remove Linked List Elements (LeetCode #203)