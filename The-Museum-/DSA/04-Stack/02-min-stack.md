# Min Stack

**Difficulty:** Medium  
**Pattern:** Stack  
**LeetCode:** #155

## Problem Statement

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:
- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element val onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

## Examples

### Example 1:
```
Input
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output
[null,null,null,null,-3,null,0,-2]

Explanation
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- Methods pop, top and getMin will always be called on non-empty stacks.
- At most `3 * 10^4` calls will be made to push, pop, top, and getMin.

## Solution Approaches

### Approach 1: Two Stacks
**Time Complexity:** O(1) for all operations  
**Space Complexity:** O(n)

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        self.stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def getMin(self):
        return self.min_stack[-1]
```

### Approach 2: Single Stack with Pairs
**Time Complexity:** O(1) for all operations  
**Space Complexity:** O(n)

```python
class MinStack:
    def __init__(self):
        self.stack = []  # Each element is (value, current_min)
    
    def push(self, val):
        if not self.stack:
            self.stack.append((val, val))
        else:
            current_min = min(val, self.stack[-1][1])
            self.stack.append((val, current_min))
    
    def pop(self):
        self.stack.pop()
    
    def top(self):
        return self.stack[-1][0]
    
    def getMin(self):
        return self.stack[-1][1]
```

### Approach 3: Single Stack with Difference
**Time Complexity:** O(1) for all operations  
**Space Complexity:** O(n)

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_val = float('inf')
    
    def push(self, val):
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            diff = val - self.min_val
            self.stack.append(diff)
            if diff < 0:
                self.min_val = val
    
    def pop(self):
        diff = self.stack.pop()
        if diff < 0:
            self.min_val = self.min_val - diff
    
    def top(self):
        diff = self.stack[-1]
        if diff > 0:
            return self.min_val + diff
        else:
            return self.min_val
    
    def getMin(self):
        return self.min_val
```

## Key Insights

1. **Track minimum** alongside each value or in separate stack
2. **Update minimum** only when new value is smaller
3. **O(1) operations** require storing extra information

## Related Problems

- Max Stack (LeetCode #716)
- Sliding Window Maximum (LeetCode #239)