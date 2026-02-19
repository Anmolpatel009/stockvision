# Linked List Cycle

**Difficulty:** Easy  
**Pattern:** Linked List  
**LeetCode:** #141

## Problem Statement

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. Note that `pos` is not passed as a parameter.

Return `true` if there is a cycle in the linked list. Otherwise, return `false`.

## Examples

### Example 1:
```
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
```

### Example 2:
```
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
```

### Example 3:
```
Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.
```

## Constraints

- The number of the nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the linked-list.

## Solution Approaches

### Approach 1: Fast and Slow Pointers (Floyd's Cycle Detection)
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def hasCycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True
```

### Approach 2: Hash Set
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def hasCycle(head):
    visited = set()
    current = head
    
    while current:
        if current in visited:
            return True
        visited.add(current)
        current = current.next
    
    return False
```

### Approach 3: Marking Visited Nodes (Modifies List)
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def hasCycle(head):
    while head:
        if head.val == float('inf'):
            return True
        head.val = float('inf')
        head = head.next
    
    return False
```

## Key Insights

1. **Floyd's algorithm** - fast pointer moves 2 steps, slow moves 1
2. **If cycle exists**, fast and slow will meet
3. **Hash set** is simpler but uses O(n) space

## Related Problems

- Linked List Cycle II (LeetCode #142)
- Happy Number (LeetCode #202)
- Find the Duplicate Number (LeetCode #287)