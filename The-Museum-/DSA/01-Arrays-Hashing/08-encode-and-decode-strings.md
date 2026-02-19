# Encode and Decode Strings

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #271

## Problem Statement

Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.

Implement `encode` and `decode` methods.

## Examples

### Example 1:
```
Input: ["lint","code","love","you"]
Output: ["lint","code","love","you"]
Explanation: One possible encode method is: "lint:;code:;love:;you"
```

### Example 2:
```
Input: ["we", "say", ":", "yes"]
Output: ["we", "say", ":", "yes"]
```

## Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` contains any possible characters out of 256 valid ASCII characters.

## Solution Approaches

### Approach 1: Length Prefix with Delimiter
**Time Complexity:** O(n) for both encode and decode  
**Space Complexity:** O(n)

```python
def encode(strs):
    result = []
    for s in strs:
        result.append(f"{len(s)}#{s}")
    return "".join(result)

def decode(s):
    result = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != '#':
            j += 1
        length = int(s[i:j])
        i = j + 1
        result.append(s[i:i + length])
        i += length
    return result
```

### Approach 2: Escape Characters
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def encode(strs):
    result = []
    for s in strs:
        escaped = s.replace('\\', '\\\\').replace(':', '\\:')
        result.append(escaped)
    return ":".join(result)

def decode(s):
    result = []
    current = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            current.append(s[i + 1])
            i += 2
        elif s[i] == ':':
            result.append("".join(current))
            current = []
            i += 1
        else:
            current.append(s[i])
            i += 1
    result.append("".join(current))
    return result
```

### Approach 3: Chunked Transfer Encoding
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def encode(strs):
    result = []
    for s in strs:
        # Store length as 4-byte integer
        length = len(s)
        result.append(length.to_bytes(4, 'big'))
        result.append(s.encode('utf-8'))
    return b''.join(result)

def decode(s):
    result = []
    i = 0
    data = s if isinstance(s, bytes) else s.encode('utf-8')
    while i < len(data):
        length = int.from_bytes(data[i:i+4], 'big')
        i += 4
        result.append(data[i:i+length].decode('utf-8'))
        i += length
    return result
```

## Key Insights

1. **Length prefix** is the most robust approach
2. **Delimiter choice** must not conflict with string content
3. **Escape characters** add complexity but allow any delimiter

## Related Problems

- Serialize and Deserialize Binary Tree (LeetCode #297)
- Serialize and Deserialize BST (LeetCode #449)
