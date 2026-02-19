# Minimum Window Substring

**Difficulty:** Hard  
**Pattern:** Sliding Window  
**LeetCode:** #76

## Problem Statement

Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `""`.

## Examples

### Example 1:
```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
```

### Example 2:
```
Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.
```

### Example 3:
```
Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
```

## Constraints

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

## Solution Approaches

### Approach 1: Sliding Window with Hash Map
**Time Complexity:** O(m + n)  
**Space Complexity:** O(1) - fixed character set

```python
from collections import Counter

def minWindow(s, t):
    if not s or not t or len(s) < len(t):
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_count = {}
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right, char in enumerate(s):
        window_count[char] = window_count.get(char, 0) + 1
        
        if char in t_count and window_count[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1
            left += 1
    
    return s[min_left:min_left + min_len] if min_len != float('inf') else ""
```

### Approach 2: Optimized with Filtered String
**Time Complexity:** O(m + n)  
**Space Complexity:** O(m)

```python
from collections import Counter

def minWindow(s, t):
    if not s or not t:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    
    # Filter s to only include characters in t
    filtered_s = [(i, char) for i, char in enumerate(s) if char in t_count]
    
    left = 0
    formed = 0
    window_count = {}
    min_len = float('inf')
    min_left = 0
    
    for right, (idx, char) in enumerate(filtered_s):
        window_count[char] = window_count.get(char, 0) + 1
        
        if window_count[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            char_start = filtered_s[left][1]
            start = filtered_s[left][0]
            
            if idx - start + 1 < min_len:
                min_len = idx - start + 1
                min_left = start
            
            window_count[char_start] -= 1
            if window_count[char_start] < t_count[char_start]:
                formed -= 1
            left += 1
    
    return s[min_left:min_left + min_len] if min_len != float('inf') else ""
```

### Approach 3: Array-based Count
**Time Complexity:** O(m + n)  
**Space Complexity:** O(128) = O(1)

```python
def minWindow(s, t):
    if not s or not t or len(s) < len(t):
        return ""
    
    count = [0] * 128
    for char in t:
        count[ord(char)] += 1
    
    required = len(t)
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right, char in enumerate(s):
        if count[ord(char)] > 0:
            required -= 1
        count[ord(char)] -= 1
        
        while required == 0:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            if count[ord(s[left])] == 0:
                required += 1
            count[ord(s[left])] += 1
            left += 1
    
    return s[min_left:min_left + min_len] if min_len != float('inf') else ""
```

## Key Insights

1. **Expand right** until window is valid
2. **Contract left** while window remains valid
3. **Track formed count** to know when window is valid

## Related Problems

- Substring with Concatenation of All Words (LeetCode #30)
- Minimum Size Subarray Sum (LeetCode #209)
- Permutation in String (LeetCode #567)