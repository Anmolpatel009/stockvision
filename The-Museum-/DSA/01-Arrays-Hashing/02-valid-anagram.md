# Valid Anagram

**Difficulty:** Easy  
**Pattern:** Arrays & Hashing  
**LeetCode:** #242

## Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1:
```
Input: s = "anagram", t = "nagaram"
Output: true
```

### Example 2:
```
Input: s = "rat", t = "car"
Output: false
```

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

## Solution Approaches

### Approach 1: Hash Map / Counter
**Time Complexity:** O(n)  
**Space Complexity:** O(1) - only 26 characters

```python
from collections import Counter

def isAnagram(s, t):
    return Counter(s) == Counter(t)
```

### Approach 2: Sorting
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def isAnagram(s, t):
    return sorted(s) == sorted(t)
```

### Approach 3: Array Count
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1
    
    return all(c == 0 for c in count)
```

## Key Insights

1. **Counter** is the most Pythonic solution
2. **Sorting** is simple but less efficient
3. **Array count** is optimal when characters are limited to lowercase letters

## Related Problems

- Group Anagrams (LeetCode #49)
- Find All Anagrams in a String (LeetCode #438)
