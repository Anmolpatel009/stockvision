# Longest Substring Without Repeating Characters

**Difficulty:** Medium  
**Pattern:** Sliding Window  
**LeetCode:** #3

## Problem Statement

Given a string `s`, find the length of the longest substring without repeating characters.

## Examples

### Example 1:
```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

### Example 2:
```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

### Example 3:
```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
```

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces.

## Solution Approaches

### Approach 1: Sliding Window with Set
**Time Complexity:** O(n)  
**Space Complexity:** O(min(m, n)) where m is charset size

```python
def lengthOfLongestSubstring(s):
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Approach 2: Sliding Window with Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(min(m, n))

```python
def lengthOfLongestSubstring(s):
    char_index = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Approach 3: Optimized with Array (ASCII)
**Time Complexity:** O(n)  
**Space Complexity:** O(128) = O(1)

```python
def lengthOfLongestSubstring(s):
    char_index = [-1] * 128  # ASCII characters
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        ascii_val = ord(char)
        if char_index[ascii_val] >= left:
            left = char_index[ascii_val] + 1
        char_index[ascii_val] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

## Key Insights

1. **Sliding window** maintains a valid substring
2. **Hash map** stores last index of each character
3. **Jump left pointer** directly when duplicate found

## Related Problems

- Longest Substring with At Most Two Distinct Characters (LeetCode #159)
- Longest Substring with At Most K Distinct Characters (LeetCode #340)
- Minimum Window Substring (LeetCode #76)