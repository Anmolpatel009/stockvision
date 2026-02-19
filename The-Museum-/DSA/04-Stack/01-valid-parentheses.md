# Valid Parentheses

**Difficulty:** Easy  
**Pattern:** Stack  
**LeetCode:** #20

## Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Examples

### Example 1:
```
Input: s = "()"
Output: true
```

### Example 2:
```
Input: s = "()[]{}"
Output: true
```

### Example 3:
```
Input: s = "(]"
Output: false
```

## Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

## Solution Approaches

### Approach 1: Stack with Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def isValid(s):
    bracket_map = {')': '(', '}': '{', ']': '['}
    stack = []
    
    for char in s:
        if char in bracket_map:
            if not stack or stack.pop() != bracket_map[char]:
                return False
        else:
            stack.append(char)
    
    return not stack
```

### Approach 2: Stack with If-Else
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def isValid(s):
    stack = []
    
    for char in s:
        if char == '(':
            stack.append(')')
        elif char == '{':
            stack.append('}')
        elif char == '[':
            stack.append(']')
        elif not stack or stack.pop() != char:
            return False
    
    return not stack
```

### Approach 3: String Replacement
**Time Complexity:** O(n²)  
**Space Complexity:** O(n)

```python
def isValid(s):
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()', '').replace('[]', '').replace('{}', '')
    return s == ''
```

## Key Insights

1. **Stack** is perfect for matching pairs
2. **Push opening brackets**, pop when closing bracket found
3. **Check stack is empty** at the end

## Related Problems

- Generate Parentheses (LeetCode #22)
- Longest Valid Parentheses (LeetCode #32)
- Remove Invalid Parentheses (LeetCode #301)