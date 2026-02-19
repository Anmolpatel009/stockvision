# Evaluate Reverse Polish Notation

**Difficulty:** Medium  
**Pattern:** Stack  
**LeetCode:** #150

## Problem Statement

Evaluate the value of an arithmetic expression in Reverse Polish Notation.

Valid operators are `+`, `-`, `*`, and `/`. Each operand may be an integer or another expression.

Note that division between two integers should truncate toward zero.

## Examples

### Example 1:
```
Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
```

### Example 2:
```
Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
```

### Example 3:
```
Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 22
```

## Constraints

- `1 <= tokens.length <= 10^4`
- `tokens[i]` is either an operator: `"+"`, `"-"`, `"*"`, or `"/"`, or an integer in the range `[-200, 200]`.

## Solution Approaches

### Approach 1: Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def evalRPN(tokens):
    stack = []
    
    for token in tokens:
        if token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))
    
    return stack[0]
```

### Approach 2: Stack with Lambda Functions
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def evalRPN(tokens):
    stack = []
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)
    }
    
    for token in tokens:
        if token in operations:
            b = stack.pop()
            a = stack.pop()
            stack.append(operations[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]
```

### Approach 3: Using Array as Stack
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def evalRPN(tokens):
    stack = []
    
    for token in tokens:
        try:
            stack.append(int(token))
        except ValueError:
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
    
    return stack[0]
```

## Key Insights

1. **RPN is naturally stack-based** - push operands, pop for operators
2. **Division truncates toward zero** - use `int(a / b)` not `a // b`
3. **Order matters** - first popped is second operand

## Related Problems

- Basic Calculator (LeetCode #224)
- Basic Calculator II (LeetCode #227)
- Basic Calculator III (LeetCode #772)