# Add Two Numbers

**Difficulty:** Medium  
**Pattern:** Linked List  
**LeetCode:** #2

## Problem Statement

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

## Examples

### Example 1:
```
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
```

### Example 2:
```
Input: l1 = [0], l2 = [0]
Output: [0]
```

### Example 3:
```
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```

## Constraints

- The number of nodes in each linked list is in the range `[1, 100]`.
- `0 <= Node.val <= 9`
- It is guaranteed that the list represents a number that does not have leading zeros.

## Solution Approaches

### Approach 1: Elementary Math
**Time Complexity:** O(max(m, n))  
**Space Complexity:** O(max(m, n))

```python
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    
    return dummy.next
```

### Approach 2: Recursive
**Time Complexity:** O(max(m, n))  
**Space Complexity:** O(max(m, n))

```python
def addTwoNumbers(l1, l2):
    def add(l1, l2, carry):
        if not l1 and not l2 and carry == 0:
            return None
        
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry
        
        node = ListNode(total % 10)
        node.next = add(
            l1.next if l1 else None,
            l2.next if l2 else None,
            total // 10
        )
        
        return node
    
    return add(l1, l2, 0)
```

### Approach 3: Convert to Numbers (Not Recommended for Large Numbers)
**Time Complexity:** O(m + n)  
**Space Complexity:** O(1)

```python
def addTwoNumbers(l1, l2):
    def list_to_num(head):
        num = 0
        multiplier = 1
        while head:
            num += head.val * multiplier
            multiplier *= 10
            head = head.next
        return num
    
    def num_to_list(num):
        if num == 0:
            return ListNode(0)
        
        dummy = ListNode(0)
        current = dummy
        while num > 0:
            current.next = ListNode(num % 10)
            current = current.next
            num //= 10
        return dummy.next
    
    total = list_to_num(l1) + list_to_num(l2)
    return num_to_list(total)
```

## Key Insights

1. **Process digit by digit** with carry
2. **Handle different lengths** by treating missing nodes as 0
3. **Don't forget final carry** if it exists

## Related Problems

- Add Two Numbers II (LeetCode #445)
- Multiply Strings (LeetCode #43)
- Plus One (LeetCode #66)